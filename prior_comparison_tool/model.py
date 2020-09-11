import prior_comparison_tool.model_conversion as mc
from bokeh.palettes import Category10
import itertools

def color_gen():
    yield from itertools.cycle(Category10[10])

colors = color_gen()
data_percentages = [90, 80,70, 60, 50, 40, 30, 20,10]

class model:
    def __init__(self, model, data, model_kwargs:dict, name='prior'):
        self.name = name
        self.color = next(colors)
        self.model_kwargs = model_kwargs
        self.model_function = model
        self.original_data = data
        self.model_arviz_data = mc.convert_full_model(model(data, **model_kwargs))
        self.posteriors = {}
        self.posterior_predictive = {}
        self.posteriors[100] = self.model_arviz_data.posterior
        self.posterior_predictive[100] = self.model_arviz_data
        for f in data_percentages:
            # loop generating the data for the varying percentages required
            p = mc.convert_posterior_model(model(data=mc.reduce_data_remove(data=data, fraction=f/100), **model_kwargs))
            # when plotting the posterior on the same plot the data needs to joined with the other models to create a 
            # pooled data set. Seems to be faster when the data is already pulled out here. Posterior predictive plot 
            # is only plotted seperately so doesn't have the same issue but does need to posterior data as well
            self.posteriors[f] = p.posterior
            self.posterior_predictive[f] = p
        
    def prior_variables(self):
        return list(self.model_arviz_data.prior.data_vars)

    def prior_predictive_variables(self):
        return list(self.model_arviz_data.prior_predictive.data_vars)

    def posterior_variables(self):
        return list(self.model_arviz_data.posterior.data_vars)

    def posterior_predictive_variables(self):
        return list(self.model_arviz_data.posterior_predictive.data_vars)