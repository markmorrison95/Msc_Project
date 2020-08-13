from prior_views.Dashboards import PriorDashboard, PosteriorDashboard, sample_trace_dashboard
from tornado.ioloop import IOLoop
import panel as pn
import param
import nest_asyncio
import functools
import webbrowser


def create_app(models={}):
    """
    Pulls together the components required to create each tab
    Initally pulls the variable names out of the data. In order to set the variable names for each dashboard
    the dashboard needs to be initialise and then have the param for variable edited with the values. This is the
    only way i could find to dynamically update with the variables as no way to pass to the class in a way that
    param.Paramatized likes

    All the components are then places into panel tabs and then the tabs object is returned
    """
    prior_vars = list(list(models.values())[0].prior.data_vars)
    posterior_vars = list(list(models.values())[0].posterior.data_vars)
    prior = PriorDashboard(name='Prior_Dashboard', data=models)
    prior.param.variable.objects = prior_vars
    prior.param.variable.default = prior_vars[0]
    # prior_predictive = PriorPredictiveDashboard(name='Prior_Predictive_Dashboard')
    # posterior = PosteriorDashboard(name='Posterior_Dashboard', data=models)
    # posterior.param.variable.objects = posterior_vars
    # posterior_predictive = posterior_predictive_Dashboard(name= 'posterior_predictive_dashboard')
    sample_trace = sample_trace_dashboard(
        name='sample_trace_dashboard', data=models)
    sample_trace.param.variable.objects = posterior_vars
    dashboard = pn.Tabs(
        ('Prior', prior.panel().servable()),
        # ('Prior_Predictive', prior_predictive.panel().servable()),
        # ('Posterior', posterior.panel().servable()),
        # ('Posterior_Predictive', posterior_predictive.panel().servable()),
        ('Sample_Trace', sample_trace.panel().servable()),
    )
    m_kwars = dict(early_rate_lambda=1, late_rate_lambda=1)
    r = pn.Row(model_selector_sliders(m_kwars), dashboard)
    return r

def add_model(event, prior_settings):
    """ config from sliders being extracted into dict, ready to be passed as 
    kwargs into a new model """
    new_config = {}
    for setting in prior_settings:
        if setting.name != 'Add Prior Setting':
            new_config[setting.name]=setting.value
    """ need to add method call for adding model config"""
    


def model_selector_sliders(prior_args:dict):
    sliders = pn.Column()
    for key, val in prior_args.items():
        upper_bound = val*1.5
        lowe_bound = val*.5
        sliders.append(pn.widgets.FloatSlider(name=key, start=lowe_bound, end=upper_bound, value=val))

    button = pn.widgets.Button(name='Add Prior Setting', button_type='primary')
    button.on_click(functools.partial(add_model, prior_settings=sliders))
    # button.on_click(add_model)
    sliders.append(button)
    return sliders




def prior_checking_tool(models={}):
    loop = IOLoop().current()
    server = pn.serve(create_app(models), show=False, loop=loop, start=False)
    # nest_asyncio required because if opening in jupyter notebooks, IOloop is already in use
    nest_asyncio.apply()
    return server
    # server.io_loop.start()
