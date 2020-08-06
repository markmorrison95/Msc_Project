from prior_views.Dashboards import PriorDashboard

def create_something_please(data, prior_views):
    prior = PriorDashboard(name='Prior_Dashboard',data=data)
    prior.variable.objects(prior_views)
    return prior.panel().servable()