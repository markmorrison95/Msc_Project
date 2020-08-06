from prior_views.Dashboards import PriorDashboard, PosteriorDashboard, sample_trace_dashboard
from tornado.ioloop import IOLoop
import panel as pn
import nest_asyncio

def create_app(models={}):
    prior_vars = list(list(models.values())[0].prior.data_vars)
    posterior_vars = list(list(models.values())[0].posterior.data_vars)
    prior = PriorDashboard(name='Prior_Dashboard',data=models)
    prior.param.variable.objects = prior_vars
    # prior_predictive = PriorPredictiveDashboard(name='Prior_Predictive_Dashboard')
    posterior = PosteriorDashboard(name='Posterior_Dashboard',data=models)
    posterior.param.variable.objects = posterior_vars
    # posterior_predictive = posterior_predictive_Dashboard(name= 'posterior_predictive_dashboard')
    sample_trace = sample_trace_dashboard(name='sample_trace_dashboard',data=models)
    sample_trace.param.variable.objects = posterior_vars
    dashboard = pn.Tabs(
                    ('Prior',prior.panel().servable()),
                    # ('Prior_Predictive', prior_predictive.panel().servable()),
                    ('Posterior', posterior.panel().servable()),
                    # ('Posterior_Predictive', posterior_predictive.panel().servable()),
                    ('Sample_Trace', sample_trace.panel().servable()),
                    )
    dashboard
    return dashboard

def prior_checking_tool(models={}):
    loop = IOLoop().current()
    nest_asyncio.apply()
    server = pn.serve(create_app(models), show=False, loop=loop, start=False, port=5006)
    server.io_loop.start()