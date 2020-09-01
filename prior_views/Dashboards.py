import param
from prior_views.Plots import prior_density_plot, posterior_density_plot, prior_predictive_density_plot, posterior_predictive_density_plot, sample_trace_plot
from prior_views.DisasterModel import CreateModel
import panel as pn
from tornado import gen
from bokeh.plotting import curdoc

# inputs_2 is the selection type for plots. Need to change name and spelling of Seperate.
inputs_2 = ['Separate Plots','Same Plot' ]


class PriorDashboard(param.Parameterized):
    # precedence less than one means it is not a user displayed option. Set through initial params passed
    data = param.Dict(precedence=-1)
    variable = param.Selector(None)
    plot_type = param.Selector(inputs_2, default=inputs_2[0])

    @param.depends('variable', 'plot_type', 'data')
    def plot(self):
        return prior_density_plot(variable=self.variable, data=self.data, plottype=self.plot_type)

    def panel(self):
        return pn.Row(self.param, self.plot, sizing_mode='scale_both')


class PriorPredictiveDashboard(param.Parameterized):
    data = param.Dict(precedence=-1)
    variable = param.Selector(None)

    @param.depends('variable', 'data')
    def plot(self):
        return prior_predictive_density_plot(variable=self.variable, data=self.data)

    def panel(self):
        return pn.Row(self.param, self.plot, sizing_mode='scale_both')


class PosteriorDashboard(param.Parameterized):
    data = param.Dict(precedence=-1)
    variable = param.Selector(None)
    plot_type = param.Selector(inputs_2, default=inputs_2[0], doc='Type of Plot:')
    percentage = param.Number(default=100, bounds=(10,100), step=10, doc='Percentage of Data:')

    @param.depends('variable', 'plot_type', 'data', 'percentage')
    def plot(self):
        return posterior_density_plot(variable=self.variable, data=self.data, percent=self.percentage, plottype=self.plot_type)


    def panel(self):
        return pn.Row(self.param, self.plot, sizing_mode='scale_both')


class posterior_predictive_Dashboard(param.Parameterized):
    data = param.Dict(precedence=-1)
    variable = param.Selector(None)

    @param.depends('variable', 'data')
    def plot(self):
        return posterior_predictive_density_plot(variable=self.variable, data=self.data)

    def panel(self):
        return pn.Row(self.param, self.plot, sizing_mode='scale_both')


class sample_trace_dashboard(param.Parameterized):
    data = param.Dict(precedence=-1)
    variable = param.Selector(None)

    @param.depends('variable', 'data')
    def plot(self):
        return sample_trace_plot(variable=self.variable, data=self.data)

    def panel(self):
        return pn.Row(self.param, self.plot, sizing_mode='scale_both')
