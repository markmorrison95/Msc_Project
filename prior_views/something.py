from prior_views.Dashboards import PriorDashboard

def create_something(data, prior_views):
    prior = PriorDashboard(name='Prior_Dashboard',data=data)
    prior.param.variable.list = prior_views
    return prior.panel().servable()