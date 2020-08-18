from prior_views.Dashboards import PriorDashboard, PosteriorDashboard, sample_trace_dashboard
from tornado.ioloop import IOLoop
import panel as pn
import param
import nest_asyncio
import functools
import webbrowser
from prior_views.models_container import model_container
from threading import Thread

def dict_to_string(dic:dict):
    s = ''
    for key, value in dic.items():
        s += (key + ' = ' + str(value) + '<br/>')
    return s

class CreateApp:
    def __init__(self, controls, models:model_container):
        self.controls = controls
        self.models = models

    def create_app(self, models:model_container):
        """
        Pulls together the components required to create each tab
        Initally pulls the variable names out of the data. In order to set the variable names for each dashboard
        the dashboard needs to be initialise and then have the param for variable edited with the values. This is the
        only way i could find to dynamically update with the variables as no way to pass to the class in a way that
        param.Paramatized likes

        All the components are then places into panel tabs and then the tabs object is returned
        """
        prior_vars = models.prior_variables()
        posterior_vars = models.posterior_variables()
        prior = PriorDashboard(name='Prior_Dashboard', data=self.models.models_dict)
        prior.param.variable.objects = prior_vars
        prior.param.variable.default = prior_vars[0]
        # prior_predictive = PriorPredictiveDashboard(name='Prior_Predictive_Dashboard')
        posterior = PosteriorDashboard(name='Posterior_Dashboard', data=self.models.models_dict)
        posterior.param.variable.objects = posterior_vars
        # posterior_predictive = posterior_predictive_Dashboard(name= 'posterior_predictive_dashboard')
        sample_trace = sample_trace_dashboard(
            name='sample_trace_dashboard', data=self.models.models_dict)
        sample_trace.param.variable.objects = posterior_vars
        dashboard = pn.Tabs(
            ('Prior', prior.panel().servable()),
            # ('Prior_Predictive', prior_predictive.panel().servable()),
            ('Posterior', posterior.panel().servable()),
            # ('Posterior_Predictive', posterior_predictive.panel().servable()),
            ('Sample_Trace', sample_trace.panel().servable()),
        )
        m_kwars = models.models_dict['Original'].model_kwargs
        prior_sliders = self.model_selector_sliders(m_kwars)
        prior_tabs = self.prior_descrip_tabs()
        prior_tabs.append(('Add Prior Config',prior_sliders))
        r = pn.Row(prior_tabs, dashboard)
        return r

    def add_model(self, event, prior_settings):
        """ config from sliders being extracted into dict, ready to be passed as 
        kwargs into a new model """
        new_config = {}
        for setting in prior_settings:
            if setting.name != 'Add Prior Setting':
                new_config[setting.name]=setting.value
        thread = Thread(target = self.controls.add_new_model_config, args = (new_config,))
        thread.start()
        webbrowser.open('https://www.youtube.com')
        """ need to add method call for adding model config"""
    
    def new_model_added(self):
        """
        Will be called after a new model has been added
        Should trigger a message saying its added or remove some sort of
        loading symbol. Then refresh the display so that the new model shows up
        """
        


    def model_selector_sliders(self, prior_args:dict):
        sliders = pn.Column()
        for key, val in prior_args.items():
            upper_bound = val*1.5
            lower_bound = val*.5
            sliders.append(pn.widgets.FloatSlider(name=key, start=lower_bound, end=upper_bound, value=val))

        button = pn.widgets.Button(name='Add Prior Setting', button_type='primary')
        button.on_click(functools.partial(self.add_model, prior_settings=sliders))
        # button.on_click(add_model)
        sliders.append(button)
        return sliders

    def prior_descrip_tabs(self):
        params={'tabs_location':'left',
        }
        tabs = pn.Tabs(**params)
        for key, val in self.models.models_dict.items():
             text = dict_to_string(val.model_kwargs)
             tabs.append((key, pn.pane.Markdown('<p>' + text + '</p>')))
        return tabs





    def prior_checking_tool(self):
        loop = IOLoop().current()
        args = {'optional argument' : '--dev'}
        server = pn.serve(self.create_app(self.models), show=False, loop=loop, start=False, **args)
        # nest_asyncio required because if opening in jupyter notebooks, IOloop is already in use
        nest_asyncio.apply()
        return server.start()
        # server.io_loop.start()
