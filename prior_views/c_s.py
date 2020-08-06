from prior_views.Dashboards import PriorDashboard

def create_sometin(data, prior_views):
    prior = PriorDashboard(name='Prior_Dashboard',data=data)
    prior.variable.objects(prior_views)
    return prior.panel().servable()