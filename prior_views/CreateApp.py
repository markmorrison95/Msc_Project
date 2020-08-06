from prior_views.Dashboards import PriorDashboard, PosteriorDashboard, sample_trace_dashboard
from tornado.ioloop import IOLoop
import panel as pn
import nest_asyncio


def create_app(models={}):
    """
    Pulls together the components required to create each tab
    Initally pulls the variable names out of the data. In order to set the variable names for each dashboard
    the dashboard needs to be initialised and then have the param for variable edited with the values. This is the
    only way i could find to dynamically update with the variables as no way to pass to the class in a way that
    param.Paramatized likes

    All the components are then places into panel tabs and then the tabs object is returned
    """
    prior_vars = list(list(models.values())[0].prior.data_vars)
    posterior_vars = list(list(models.values())[0].posterior.data_vars)
    prior = PriorDashboard(name='Prior_Dashboard', data=models)
    prior.param.variable.objects = prior_vars
    # prior_predictive = PriorPredictiveDashboard(name='Prior_Predictive_Dashboard')
    posterior = PosteriorDashboard(name='Posterior_Dashboard', data=models)
    posterior.param.variable.objects = posterior_vars
    # posterior_predictive = posterior_predictive_Dashboard(name= 'posterior_predictive_dashboard')
    sample_trace = sample_trace_dashboard(
        name='sample_trace_dashboard', data=models)
    sample_trace.param.variable.objects = posterior_vars
    dashboard = pn.Tabs(
        ('Prior', prior.panel().servable()),
        # ('Prior_Predictive', prior_predictive.panel().servable()),
        ('Posterior', posterior.panel().servable()),
        # ('Posterior_Predictive', posterior_predictive.panel().servable()),
        ('Sample_Trace', sample_trace.panel().servable()),
    )
    dashboard
    return dashboard


def prior_checking_tool(models={}):
    loop = IOLoop().current()
    server = pn.serve(create_app(models), show=False, loop=loop, start=False)
    # nest_asyncio required because if opening in jupyter notebooks, IOloop is already in use
    nest_asyncio.apply()
    return server
    # server.io_loop.start()
