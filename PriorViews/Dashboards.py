import param
from Plots import prior_density_plot, posterior_density_plot
from Models.DisasterModel import CreateModel


pm_data = DisasterModel.CreateModel()

prior_inputs = list(pm_data.prior.data_vars)
posterior_inputs = list(pm_data.prior.data_vars)
inputs_2 = ['Same Plot', 'Seperate Plots']

    
class PriorDashboard(param.Parameterized):
    variable = param.Selector(prior_inputs, default=prior_inputs[0])
    plot_type = param.Selector(inputs_2, default=inputs_2[0])
    
    @param.depends('variable', 'plot_type')
    def plot(self):
        return p.prior_density_plot(variable=self.variable, data=models, plottype=self.plot_type)
    
    def panel(self):
        return pn.Row(self.param, self.plot)



class PosteriorDashboard(param.Parameterized):
    variable = param.Selector(prior_inputs, default=prior_inputs[0])
    plot_type = param.Selector(inputs_2, default=inputs_2[0])
    
    @param.depends('variable', 'plot_type')
    def plot(self):
        return posterior_density_plot(variable=self.variable, data=models, plottype=self.plot_type)
    
    def panel(self):
        return pn.Row(self.param, self.plot)


dashboard = pn.Tab('Prior',(PriorDashboard(name='Prior_Dashboard')),('Posterior', (PosteriorDashboard(name='Posterior_Dashboard'))))
pn.serve(dashboard.panel().servable())