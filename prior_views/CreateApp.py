from prior_views.Dashboards import PriorDashboard

def create_app():
    prior = PriorDashboard(name='Prior_Dashboard')
    prior_predictive = PriorPredictiveDashboard(name='Prior_Predictive_Dashboard')
    posterior = PosteriorDashboard(name='Posterior_Dashboard')
    posterior_predictive = posterior_predictive_Dashboard(name= 'posterior_predictive_dashboard')
    sample_trace = sample_trace_dashboard(name='sample_trace_dashboard')
    dashboard = pn.Tabs(
                    ('Prior',prior.panel().servable()),
                    # ('Prior_Predictive', prior_predictive.panel().servable()),
                    ('Posterior', posterior.panel().servable()),
                    # ('Posterior_Predictive', posterior_predictive.panel().servable()),
                    ('Sample_Trace', sample_trace.panel().servable()),
                    )
    dashboard
    return dashboard

def create_prior_view(data, prior_views):
    prior = PriorDashboard(data=data, name='Prior_Dashboard')
    return prior.panel().servable()


# posterior_predictive_inputs = list(pm_data.posterior_predictive.data_vars)
# loop = IOLoop().current()
# server = pn.serve(create_app, show=False, loop=loop, start=False, port=5006)
# server.io_loop.start()