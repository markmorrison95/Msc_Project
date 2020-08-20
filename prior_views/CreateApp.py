from prior_views.Dashboards import PriorDashboard, PosteriorDashboard, sample_trace_dashboard, PriorPredictiveDashboard, posterior_predictive_Dashboard
from tornado.ioloop import IOLoop
import panel as pn
import param
import nest_asyncio
import functools
import webbrowser
from prior_views.models_container import model_container
from threading import Thread
from webcolors import hex_to_rgb


def dict_to_string(dic: dict):
    s = ''
    for key, value in dic.items():
        s += (key + ' = ' + str(value) + '<br/>')
    return s


class CreateApp:
    def __init__(self, controls, models: model_container):
        self.controls = controls
        self.models = models
        """
        Pulls together the components required to create each tab
        Initally pulls the variable names out of the original_model. In order to set the variable names for each dashboard
        the dashboard needs to be initialise and then have the param for variable edited with the values. This is the
        only way i could find to dynamically update with the variables as no way to pass to the class in a way that
        param.Paramatized likes

        All the components are then places into panel tabs and then the tabs object is returned
        """
        prior_vars = self.models.original_model.prior_variables()
        posterior_vars = self.models.original_model.posterior_variables()
        prior_predictive_vars = self.models.original_model.prior_predictive_variables()
        posterior_predictive_vars = self.models.original_model.posterior_predictive_variables()
        prior = PriorDashboard(name='Prior_Dashboard',
                               data=self.models.models_dict,
                               )
        prior.param.variable.objects = prior_vars
        prior.panel()
        prior_predictive = PriorPredictiveDashboard(
            name='Prior_Predictive_Dashboard',
            data=self.models.models_dict,
            )
        prior_predictive.param.variable.objects = prior_predictive_vars
        posterior = PosteriorDashboard(
            name='Posterior_Dashboard', 
            data=self.models.models_dict
            )
        posterior.param.variable.objects = posterior_vars
        posterior.panel()
        posterior_predictive = posterior_predictive_Dashboard(
            name= 'posterior_predictive_dashboard',
            data=self.models.models_dict,
            )
        posterior_predictive.param.variable.objects = posterior_predictive_vars
        sample_trace = sample_trace_dashboard(
            name='sample_trace_dashboard',
            data=self.models.models_dict,
            )
        sample_trace.param.variable.objects = posterior_vars
        dashboard = pn.Tabs(
            ('Prior', prior.panel().servable()),
            ('Prior_Predictive', prior_predictive.panel().servable()),
            ('Posterior', posterior.panel().servable()),
            ('Posterior_Predictive', posterior_predictive.panel().servable()),
            ('Sample_Trace', sample_trace.panel().servable()),
        )
        m_kwars = self.models.models_dict['Original'].model_kwargs
        self.prior_sliders = self.model_selector_sliders(m_kwars)
        self.prior_tabs = self.prior_descrip_tabs()
        self.prior_tabs.append(('Add Prior Config', self.prior_sliders))
        model_config_column = pn.Column(pn.pane.Markdown('<h2>Model Configurations:<h2>'), self.prior_tabs)
        model_plots_column = pn.Column(pn.pane.Markdown('<h2>Model Plots:<h2>'), dashboard)
        self.r = pn.Row(model_config_column, model_plots_column)






    def add_model(self, event, prior_settings):
        """ config from sliders being extracted into dict, ready to be passed as 
        kwargs into a new model """
        new_config = {}
        model_name = ""
        for setting in prior_settings:
            if setting.name != 'Add Prior Setting':
                if setting.name == 'Prior Config Name:':
                    model_name = setting.value
                else:
                    new_config[setting.name] = setting.value
        self.prior_sliders[len(self.prior_sliders)-1].disabled = True
        self.prior_sliders.append(
            pn.widgets.Progress(
                name='Sampling In Progress',
                active=True,
                bar_color='info',
                width=320,
            )
        )
        thread = Thread(
            target=self.controls.add_new_model_config,
            args=(new_config, model_name)
        )
        thread.start()
        """ need to add method call for adding model config"""





    def new_model_added(self, new_prior_model):
        """
        Will be called after a new model has been added
        Should trigger a message saying its added or remove some sort of
        loading symbol. Then refresh the display so that the new model shows up
        """
        self.prior_sliders.remove(
            self.prior_sliders[len(self.prior_sliders)-1])
        self.prior_sliders[len(self.prior_sliders)-1].disabled = False
        self.prior_tabs.insert(
            (len(self.prior_tabs)-1),
            (new_prior_model.name, self.prior_config_view(
                                                original_prior_args=self.models.original_model.model_kwargs,
                                                new_prior_args=new_prior_model.model_kwargs,
                                                new_model_name=new_prior_model.name,
                                                color=new_prior_model.color
            )
            )
        )




    def prior_config_view(self, original_prior_args, new_prior_args, new_model_name, color):
        sliders = pn.Column()
        sliders.append(pn.widgets.StaticText(
                                name='Model Config Name', 
                                value=new_model_name
                                )
                            )
        for (key, val), (key2, val2) in zip(original_prior_args.items(), new_prior_args.items()):
            upper_bound = val*1.5
            lower_bound = val*.5
            sliders.append(
                pn.widgets.FloatSlider(
                    name=key,
                    start=lower_bound,
                    end=upper_bound,
                    value=val2,
                    disabled=True,
                )
            )
        sliders.append(pn.widgets.ColorPicker(value=color, disabled=True))
        return sliders




    def model_selector_sliders(self, prior_args: dict):
        sliders = pn.Column()
        sliders.append(pn.widgets.TextInput(
            name='Prior Config Name:', value=('eg. Prior 1')))
        for key, val in prior_args.items():
            upper_bound = val*1.5
            lower_bound = val*.5
            sliders.append(
                pn.widgets.FloatSlider(
                                    name=key, 
                                    start=lower_bound, 
                                    end=upper_bound, 
                                    value=val,
                                    step=.01,
                                    )
                            )

        button = pn.widgets.Button(
            name='Add Prior Setting', button_type='primary')
        button.on_click(functools.partial(
            self.add_model, prior_settings=sliders))
        # button.on_click(add_model)
        sliders.append(button)
        return sliders





    def prior_descrip_tabs(self):
        params = {'tabs_location': 'left',
                  }
        tabs = pn.Tabs(**params)
        for key, val in self.models.models_dict.items():
            tabs.append(
                (key, 
                self.prior_config_view(
                    original_prior_args=val.model_kwargs,
                    new_prior_args=val.model_kwargs,
                    new_model_name=key,
                    color=val.color,
                )
                )
            )
        return tabs






    def prior_checking_tool(self):
        loop = IOLoop().current()
        args = {'optional argument': '--dev'}
        server = pn.serve(self.r, show=False, loop=loop, start=False, **args)
        # nest_asyncio required because if opening in jupyter notebooks, IOloop is already in use
        nest_asyncio.apply()
        return server.start()
        # server.io_loop.start()
