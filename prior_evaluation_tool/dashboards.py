import param
from prior_evaluation_tool.plots import prior_density_plot, posterior_density_plot, prior_predictive_density_plot, posterior_predictive_density_plot, sample_trace_plot, compare_plot
import panel as pn
from tornado import gen
from bokeh.plotting import curdoc

# inputs is the selection type for plots. Need to change name and spelling of Seperate.
inputs = ['Separate Plots','Same Plot' ]


class priorDashboard(param.Parameterized):
    """
    Dashboard for the prior view

    data should be dictionary of model objects
    and should be set on instantiation along with the name
    variable needs to be set with the prior variables list after instantiation

    returns a panel row with the parameter controls and the plots
    """
    # precedence less than one means it is not a user displayed option. Set through initial params passed
    data = param.Dict(precedence=-1)
    variable = param.Selector(None)
    plot_type = param.Selector(inputs, default=inputs[0])

    @param.depends('variable', 'plot_type', 'data')
    def plot(self):
        return prior_density_plot(variable=self.variable, data=self.data, plottype=self.plot_type)

    def panel(self):
        return pn.Row(self.param, self.plot, sizing_mode='scale_both')


class priorPredictiveDashboard(param.Parameterized):
    """
    Dashboard for the prior predictive view

    data should be dictionary of model objects
    and should be set on instantiation along with the name
    variable needs to be set with the posterior variables list after instantiation

    returns a panel row with the parameter controls and the plots
    """
    data = param.Dict(precedence=-1)
    variable = param.Selector(None)

    @param.depends('variable', 'data')
    def plot(self):
        return prior_predictive_density_plot(variable=self.variable, data=self.data)

    def panel(self):
        return pn.Row(self.param, self.plot, sizing_mode='scale_both')


class posteriorDashboard(param.Parameterized):
    """
    Dashboard for the posterior view

    data should be dictionary of model objects
    and should be set on instantiation along with the name
    variable needs to be set with the posterior variables list after instantiation

    returns a panel row with the parameter controls and the plots
    """
    data = param.Dict(precedence=-1)
    variable = param.Selector(None)
    plot_type = param.Selector(inputs, default=inputs[0], doc='Type of Plot:')
    percentage = param.Number(default=100, bounds=(10,100), step=10, doc='Percentage of Data:')

    @param.depends('variable', 'plot_type', 'data', 'percentage')
    def plot(self):
        return posterior_density_plot(variable=self.variable, data=self.data, percent=self.percentage, plottype=self.plot_type)


    def panel(self):
        return pn.Row(self.param, self.plot, sizing_mode='scale_both')


class posteriorPredictiveDashboard(param.Parameterized):
    """
    Dashboard for the posterior predictive view

    data should be dictionary of model objects
    and should be set on instantiation along with the name
    variable needs to be set with the posterior variables list after instantiation

    returns a panel row with the parameter controls and the plots
    """
    data = param.Dict(precedence=-1)
    variable = param.Selector(None)
    percentage = param.Number(default=100, bounds=(10,100), step=10, doc='Percentage of Data:')

    @param.depends('variable', 'data', 'percentage')
    def plot(self):
        return posterior_predictive_density_plot(variable=self.variable, data=self.data, percent=self.percentage)

    def panel(self):
        return pn.Row(self.param, self.plot, sizing_mode='scale_both')


class sampleTraceDashboard(param.Parameterized):
    """
    Dashboard for the MCMC trace view

    data should be dictionary of model objects
    and should be set on instantiation along with the name
    variable needs to be set with the posterior variables list after instantiation

    returns a panel row with the parameter controls and the plots
    """
    data = param.Dict(precedence=-1)
    variable = param.Selector(None)

    @param.depends('variable', 'data')
    def plot(self):
        return sample_trace_plot(variable=self.variable, data=self.data)

    def panel(self):
        return pn.Row(self.param, self.plot, sizing_mode='scale_both')

class waicCompareDashboard(param.Parameterized):
    """
    Dashboard for the WAIC trace view

    data should be dictionary of model objects
    and should be set on instantiation along with the name
    variable needs to be set with the posterior variables list after instantiation

    returns a panel row with the parameter controls and the plots
    """
    data = param.Dict(precedence=-1)

    @param.depends('data')
    def plot(self):
        return compare_plot(data=self.data)

    def panel(self):
        return pn.Row(self.param, pn.Column(self.plot), sizing_mode='scale_both')
