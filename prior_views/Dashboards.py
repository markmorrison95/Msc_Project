import param
from prior_views.Plots import prior_density_plot, posterior_density_plot, prior_predictive_density_plot, posterior_predictive_density_plot, sample_trace_plot
from prior_views.DisasterModel import CreateModel
import panel as pn
from tornado import gen
from bokeh.plotting import curdoc
from prior_views.ModelConversion import convert_models

inputs_2 = ['Same Plot', 'Seperate Plots']
default_selectors = [None, None, None]

    
class PriorDashboard(param.Parameterized):
    data = param.Dict(precedence=-1)
    variable = param.Selector(default_selectors)
    plot_type = param.Selector(inputs_2, default=inputs_2[0])
    
    @param.depends('variable', 'plot_type', 'data')
    def plot(self):
        return prior_density_plot(variable=self.variable, data=self.data, plottype=self.plot_type)
    
    def panel(self):
        return pn.Row(self.param, self.plot)

class PriorPredictiveDashboard(param.Parameterized):
    data = param.Dict(precedence=-1)
    variable = param.Selector(default_selectors)
    plot_type = param.Selector(inputs_2, default=inputs_2[0])
    
    @param.depends('variable', 'data')
    def plot(self):
        return prior_predictive_density_plot(variable=self.variable, data=self.data)
    
    def panel(self):
        return pn.Row(self.param, self.plot)



class PosteriorDashboard(param.Parameterized):
    data = param.Dict(precedence=-1)
    variable = param.Selector(default_selectors)
    plot_type = param.Selector(inputs_2, default=inputs_2[0])
    
    @param.depends('variable', 'plot_type', 'data')
    def plot(self):
        return posterior_density_plot(variable=self.variable, data=self.data, plottype=self.plot_type)
    
    def panel(self):
        return pn.Row(self.param, self.plot)

class posterior_predictive_Dashboard(param.Parameterized):
    data = param.Dict(precedence=-1)
    variable = param.Selector(default_selectors)
    
    @param.depends('variable', 'data')
    def plot(self):
        return posterior_predictive_density_plot(variable=self.variable, data=self.data)
    
    def panel(self):
        return pn.Row(self.param, self.plot)

class sample_trace_dashboard(param.Parameterized):
    data = param.Dict(precedence=-1)
    variable = param.Selector(default_selectors)
    
    @param.depends('variable', 'data')
    def plot(self):
        return sample_trace_plot(variable=self.variable, data=self.data)
    
    def panel(self):
        return pn.Row(self.param, self.plot)