import param
from prior_views.Plots import prior_density_plot, posterior_density_plot, prior_predictive_density_plot, posterior_predictive_density_plot, sample_trace_plot
from prior_views.DisasterModel import CreateModel
import panel as pn
from tornado import gen
from tornado.ioloop import IOLoop
from bokeh.plotting import curdoc
from prior_views.ModelConversion import convert_models

# pm_data = CreateModel()
# data = {'Prior_1': pm_data, 'Prior_2': pm_data}
# data = {}
# pm_data = list(data.values())[0]
# prior_inputs = list(pm_data.prior.data_vars)
# prior_predictive_inputs = list(pm_data.prior_predictive.data_vars)
# posterior_inputs = list(pm_data.posterior.data_vars)
# posterior_predictive_inputs = list(pm_data.posterior_predictive.data_vars)
inputs_2 = ['Same Plot', 'Seperate Plots']
prior_inputs = ['switchpoint','early_rate', 'late_rate']

    
class PriorDashboard(param.Parameterized):
    data = param.Dict(precedence=-1)
    variable = param.Selector(prior_inputs, default=prior_inputs[0])
    plot_type = param.Selector(inputs_2, default=inputs_2[0])
    
    @param.depends('variable', 'plot_type', 'data')
    def plot(self):
        return prior_density_plot(variable=self.variable, data=self.data, plottype=self.plot_type)
    
    def panel(self):
        return pn.Row(self.param, self.plot)

# class PriorPredictiveDashboard(param.Parameterized):
#     variable = param.Selector(prior_predictive_inputs, default=prior_predictive_inputs[0])
#     plot_type = param.Selector(inputs_2, default=inputs_2[0])
    
#     @param.depends('variable')
#     def plot(self):
#         return prior_predictive_density_plot(variable=self.variable, data=data)
    
#     def panel(self):
#         return pn.Row(self.param, self.plot)



# class PosteriorDashboard(param.Parameterized):
#     variable = param.Selector(posterior_inputs, default=posterior_inputs[0])
#     plot_type = param.Selector(inputs_2, default=inputs_2[0])
    
#     @param.depends('variable', 'plot_type')
#     def plot(self):
#         return posterior_density_plot(variable=self.variable, data=data, plottype=self.plot_type)
    
#     def panel(self):
#         return pn.Row(self.param, self.plot)

# class posterior_predictive_Dashboard(param.Parameterized):
#     variable = param.Selector(posterior_predictive_inputs, default=posterior_predictive_inputs[0])
    
#     @param.depends('variable')
#     def plot(self):
#         return posterior_predictive_density_plot(variable=self.variable, data=data)
    
#     def panel(self):
#         return pn.Row(self.param, self.plot)

# class sample_trace_dashboard(param.Parameterized):
#     variable = param.Selector(posterior_inputs, default=posterior_inputs[0])
    
#     @param.depends('variable')
#     def plot(self):
#         return sample_trace_plot(variable=self.variable, data=data)
    
#     def panel(self):
#         return pn.Row(self.param, self.plot)

# prior = PriorDashboard(name='Prior_Dashboard', data={'key':'value'}, prior_inputs=['switchpoint'])
# prior.panel().servable()