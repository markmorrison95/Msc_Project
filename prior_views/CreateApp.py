from prior_views.Dashboards import PriorDashboard, PosteriorDashboard, sample_trace_dashboard, PriorPredictiveDashboard, posterior_predictive_Dashboard
from tornado.ioloop import IOLoop
import panel as pn
import param
import nest_asyncio
import functools
import webbrowser
from prior_views.models_container import model_container
from threading import Thread


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
        self.prior = PriorDashboard(name='Prior_Dashboard',
                               data=self.models.models_dict,
                               )
        self.prior.param.variable.objects = prior_vars
        self.prior.set_default(param_name='variable', value=prior_vars[0])
        self.prior_predictive = PriorPredictiveDashboard(
            name='Prior_Predictive_Dashboard',
            data=self.models.models_dict,
            )
        self.prior_predictive.param.variable.objects = prior_predictive_vars
        self.prior_predictive.set_default(param_name='variable', value=prior_predictive_vars[0])
        self.posterior = PosteriorDashboard(
            name='Posterior_Dashboard', 
            data=self.models.models_dict
            )
        self.posterior.param.variable.objects = posterior_vars
        self.posterior.set_default(param_name='variable', value=posterior_vars[0])
        self.posterior_predictive = posterior_predictive_Dashboard(
            name= 'posterior_predictive_dashboard',
            data=self.models.models_dict,
            )
        self.posterior_predictive.param.variable.objects = posterior_predictive_vars
        self.posterior_predictive.set_default(param_name='variable', value=posterior_predictive_vars[0])
        self.sample_trace = sample_trace_dashboard(
            name='sample_trace_dashboard',
            data=self.models.models_dict,
            )
        self.sample_trace.param.variable.objects = posterior_vars
        self.sample_trace.set_default(param_name='variable', value=posterior_vars[0])
        dashboard = pn.Tabs(
            ('Prior', self.prior.panel().servable()),
            ('Prior_Predictive', self.prior_predictive.panel().servable()),
            ('Posterior', self.posterior.panel().servable()),
            ('Posterior_Predictive', self.posterior_predictive.panel().servable()),
            ('Sample_Trace', self.sample_trace.panel().servable()),
        )
        m_kwars = self.models.models_dict['Original'].model_kwargs
        self.prior_sliders = self.model_selector_sliders(m_kwars)
        self.prior_tabs = self.prior_descrip_tabs()
        self.prior_tabs.append(('Add Prior Config', self.prior_sliders))
        model_config_column = pn.Column(pn.pane.Markdown('<h2>Model Configurations:<h2>'), self.prior_tabs)
        model_plots_column = pn.Column(pn.pane.Markdown('<h2>Model Plots:<h2>'), dashboard)
        self.r = pn.Row(model_config_column, model_plots_column)






    # ************* boolean flag and warning label for empty name and sampling failed *********
    """class variables so that flag is mantained outside of method and the alert message can
        be easily removed from the display by removing from list by reference"""
    name_empty_flag = False
    name_empty_alert = pn.widgets.StaticText(value='Add Prior Name before Submitting')

    sampling_failed_flag = False
    sampling_failed_alert = pn.widgets.StaticText(value='Sampling failed, try another config')
    # ********************************************************************************************

    # ******* loading bar for when sampling is taking place *******
    loading_bar = pn.widgets.Progress(
                    name='Sampling In Progress',
                    active=True,
                    bar_color='info',
                    width=300,)
    # **************************************************************




    def add_model(self, event, prior_settings, name):
        """ config from sliders being extracted into dict, ready to be passed as 
        kwargs into a new model """
        if self.sampling_failed_flag:
            self.prior_sliders.remove(self.sampling_failed_alert)
            self.sampling_failed_flag = False
        if not name.value:
            # checking if name has been left blank
            if not self.name_empty_flag:
                # checks if repeated offense. 
                # If not will display warning, otherwise warning will just remain in place
                self.prior_sliders.append(self.name_empty_alert)
                self.name_empty_flag = True
        else:
            if self.name_empty_flag:
            # checks for empty name warning. If exists removes the label and resets flag and then continues
                self.prior_sliders.remove(self.name_empty_alert)
                self.name_empty_flag = False

            new_config = {}
            model_name = ""
            for setting in prior_settings:
                if setting.name != 'Add Prior Setting':
                    if setting.name == 'Prior Config Name:':
                        model_name = setting.value
                    else:
                        new_config[setting.name] = setting.value
            self.button.disabled = True
            self.prior_sliders.append(self.loading_bar)
            thread = Thread(
                target=self.controls.add_new_model_config,
                args=(new_config, model_name)
            )
            thread.start()


    def sampling_failed(self):
        self.prior_sliders.remove(self.loading_bar)
        self.prior_sliders.append(self.sampling_failed_alert)
        self.sampling_failed_flag = True
        self.button.disabled = False





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
        # ************ triggers a reload of param classes producing plots ***********
        pram = ['variable',]
        self.prior.param.trigger(*pram)
        self.prior_predictive.param.trigger(*pram)
        self.posterior.param.trigger(*pram)
        self.posterior_predictive.param.trigger(*pram)
        self.sample_trace.param.trigger(*pram)
        # *******************************************************************************
        




    def prior_config_view(self, original_prior_args, new_prior_args, new_model_name, color):
        sliders = pn.Column()
        sliders.append(pn.widgets.StaticText(
                                name='Model Config Name', 
                                value=new_model_name
                                )
                            )
        for (key, val), (key2, val2) in zip(original_prior_args.items(), new_prior_args.items()):
            if val != 0:
                upper_bound = val*3
                lower_bound = val-(val*2)
            else:
            # if value is 0 then cant change by multiplying value
            # fixed at -50 50. might not be best solution but current fix
                upper_bound = 50
                lower_bound = -50
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



    button = pn.widgets.Button(
            name='Add Prior Setting', button_type='primary')

    def model_selector_sliders(self, prior_args: dict):
        sliders = pn.Column()
        name_box = pn.widgets.TextInput(
                name='Prior Config Name:', 
                placeholder=('eg. Prior 1'))
        sliders.append(name_box)
        for key, val in prior_args.items():
            if val != 0:
                upper_bound = val*3
                lower_bound = val-(val*2)
            else:
                upper_bound = 20
                lower_bound = -20
            sliders.append(
                pn.widgets.FloatSlider(
                                    name=key, 
                                    start=lower_bound, 
                                    end=upper_bound, 
                                    value=val,
                                    step=.01,
                                    )
                            )

        self.button.on_click(functools.partial(
            self.add_model, prior_settings=sliders, name=name_box))
        # button.on_click(add_model)
        sliders.append(self.button)
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
        return server.run_until_shutdown()
        # server.io_loop.start()
