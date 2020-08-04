import panel as pn


class Tabs:

    def __init__(self, model, plots):
        self.models = models
        self.plots = plots

    pn.extension()

    radio_group = pn.widgets.RadioButtonGroup(
        name='Radio Button Group', options=['Same Plot', 'Seperate Plots'], button_type='success')

    def prior_view_tab(self):
        kw = dict(variable=sorted(list(list(self.models.values())[0].prior.data_vars)), plottype=radio_group)
        i = pn.interact(self.plots.prior_density_plot, **kw)
        text = "Hey"
        p = pn.Row(text,pn.Row(pn.Column(i[0][0],i[0][1]),i[1]))
        return p



    def posterior_view_tab(self):
        kw = dict(variable=sorted(list(list(self.models.values())[0].posterior.data_vars)),plottype=radio_group)
        i = pn.interact(self.plots.posterior_density_plot, **kw)
        text = "Hey"
        p = pn.Row(text,pn.Row(pn.Column(i[0][0],i[0][1]),i[1]))
        return p

    def prior_predictive_view_tab(self):
        kw = dict(variable=sorted(list(list(self.models.values())[0].prior_predictive.data_vars)))
        i = pn.interact(self.plots.prior_predictive_density_plot, **kw)
        text = "Hey"
        p = pn.Row(text,pn.Row(i[0],i[1]))
        return p

    def posterior_predictive_view_tab(self):
        kw = dict(variable=sorted(list(list(self.models.values())[0].posterior_predictive.data_vars)))
        i = pn.interact(self.plots.posterior_predictive_density_plot, **kw)
        text = "Hey"
        p = pn.Row(text,pn.Row(i[0],i[1]))
        return p

    def sample_trace_view_tab(self):
        kw = dict(variable=sorted(list(list(self.models.values())[0].posterior.data_vars)))
        i = pn.interact(self.plots.sample_trace_plot, **kw)
        text = "Hey"
        p = pn.Row(text,pn.Row(i[0],i[1]))
        return p