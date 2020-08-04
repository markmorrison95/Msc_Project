class ViewConstructor:

    def final_view(self, tabs):
        tabs = pn.Tabs(('Prior',tabs.prior_view_tab),('Posterior', tabs.posterior_view_tab),('Posterior Predictive',tabs.posterior_predictive_view_tab),('Sample Trace', tabs.sample_trace_view_tab))
        return tabs