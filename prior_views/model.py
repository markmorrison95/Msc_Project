import prior_views.ModelConversion as mc

data_percentages = [95, 90,85, 80]

class model:
    def __init__(self, model, data, model_kwargs:dict):
        self.model_kwargs = model_kwargs
        self.model_function = model
        self.original_data = data
        self.model_arviz_data = mc.convert_full_model(model(data, **model_kwargs))
        self.posteriors = {}
        self.posteriors[100] = self.model_arviz_data.posterior
        for f in data_percentages:
            p = mc.convert_posterior_model(model(data=mc.data_reduce_with_nan(data, f/100), **model_kwargs))
            self.posteriors[f] = p.posterior
        
    def prior_variables(self):
        return list(self.model_arviz_data.prior.data_vars)

    def posterior_variables(self):
        return list(self.model_arviz_data.prior.data_vars)