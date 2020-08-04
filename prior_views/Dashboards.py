import param
from Plots import prior_density_plot, posterior_density_plot
from DisasterModel import CreateModel
import panel as pn

pm_data = CreateModel()
data = {'Prior_1': pm_data, 'Prior_2': pm_data}
prior_inputs = list(pm_data.prior.data_vars)
posterior_inputs = list(pm_data.prior.data_vars)
inputs_2 = ['Same Plot', 'Seperate Plots']

    
class PriorDashboard(param.Parameterized):
    variable = param.Selector(prior_inputs, default=prior_inputs[0])
    plot_type = param.Selector(inputs_2, default=inputs_2[0])
    
    @param.depends('variable', 'plot_type')
    def plot(self):
        return prior_density_plot(variable=self.variable, data=data, plottype=self.plot_type)
    
    def panel(self):
        return pn.Row(self.param, self.plot)



class PosteriorDashboard(param.Parameterized):
    variable = param.Selector(prior_inputs, default=prior_inputs[0])
    plot_type = param.Selector(inputs_2, default=inputs_2[0])
    
    @param.depends('variable', 'plot_type')
    def plot(self):
        return posterior_density_plot(variable=self.variable, data=data, plottype=self.plot_type)
    
    def panel(self):
        return pn.Row(self.param, self.plot)


prior = PriorDashboard(name='Prior_Dashboard')
posterior = PosteriorDashboard(name='Posterior_Dashboard')
dashboard = pn.Tabs(   ('Prior',prior.panel().servable()) ,  ('Posterior', posterior.panel().servable())   )
pn.serve(dashboard)