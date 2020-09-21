import prior_evaluation_tool.model_conversion as mc
from bokeh.palettes import Category10
import itertools

# cycles through a selection of bokeh colors to assign each model
# mantained outside of class so as to be independent of model instantiation
def color_gen():
    yield from itertools.cycle(Category10[10])

colors = color_gen()

data_percentages = [90, 80,70, 60, 50, 40, 30, 20,10]

class model:
    """
    object for storing all the model related data

    @params
    model = the model method for creation 
    data = pandas series of dataframe for model
    InferenceData_dims = arviz dims dict
    InferenceData_coords = arviz coords dict
    num_samples_pymc3 = number of samples for MCMC sampling with pymc3
    model_kwargs = dict of the prior paramters for the model methods
    name = configuration name
    

    one instantiation will fit the model and create the inference data
    inference data for the @data_percentages will be stored in a dict for the posterior & pp samples

    all sampling is outsourced to model conversion
    """
    def __init__(self, model, data, InferenceData_dims,InferenceData_coords, num_samples_pymc3, model_kwargs:dict, name='prior'):
        self.name = name
        self.color = next(colors)
        self.model_kwargs = model_kwargs
        self.model_function = model
        self.original_data = data
        self.num_samples_pymc3=num_samples_pymc3
        self.InferenceData_coords=InferenceData_coords
        self.InferenceData_dims=InferenceData_dims


        self.model_arviz_data = mc.convert_full_model(
            model=model(data, **model_kwargs),
            num_samples=num_samples_pymc3,
            InferenceData_coords=InferenceData_coords,
            InferenceData_dims=InferenceData_dims,
            )
        self.posteriors = {}
        self.posterior_predictive = {}
        self.posteriors[100] = self.model_arviz_data.posterior
        self.posterior_predictive[100] = self.model_arviz_data
        for f in data_percentages:
            # loop generating the data for the varying percentages required
            p = mc.convert_posterior_model(
                model = model(data=mc.reduce_data_remove(data=data, fraction=f/100), **model_kwargs),
                num_samples=num_samples_pymc3,
                InferenceData_coords=InferenceData_coords,
                InferenceData_dims=InferenceData_dims,
                )
            # when plotting the posterior on the same plot the data needs to joined with the other models to create a 
            # pooled data set. Seems to be faster when the data is already pulled out here. Posterior predictive plot 
            # is only plotted seperately so doesn't have the same issue but does need to posterior data as well so stored
            # seperately when so as to improve plot creation speed slightly
            self.posteriors[f] = p.posterior
            self.posterior_predictive[f] = p





   
        
    # ******* methods creating a list of the variables of type function name **************
    # used for creating the drop down variable selectors in the dashboards
    def prior_variables(self):
        return list(self.model_arviz_data.prior.data_vars)

    def prior_predictive_variables(self):
        return list(self.model_arviz_data.prior_predictive.data_vars)

    def posterior_variables(self):
        return list(self.model_arviz_data.posterior.data_vars)

    def posterior_predictive_variables(self):
        return list(self.model_arviz_data.posterior_predictive.data_vars)
    # ***************************************************************************************