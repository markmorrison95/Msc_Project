import arviz as az
import matplotlib.pyplot as plt
import numpy as np
import pymc3 as pm
import pandas as pd
from prior_evaluation_tool.main import create_app


size = 200
true_intercept = 1
true_slope = 2

x = np.linspace(0, 1, size)
# y = a + b*x
true_regression_line = true_intercept + true_slope * x
# add noise
y = true_regression_line + np.random.normal(scale=.5, size=size)

data = pd.DataFrame()
data['y'] = y
data['x'] = x


def model_method(data, **prior_kwargs):
    with pm.Model() as model: # model specifications in PyMC3 are wrapped in a with-statement
        # Define priors
        sigma = pm.HalfCauchy('sigma', beta=prior_kwargs['sigma beta'], testval=prior_kwargs['sigma testval'])
        intercept = pm.Normal('intercept', mu=prior_kwargs['intercept mu'], sigma=prior_kwargs['intercept sigma'])
        x_coeff = pm.Normal('x', mu=prior_kwargs['x mu'], sigma=prior_kwargs['x sigma'])

        # Define likelihood
        likelihood = pm.Normal('y', mu=intercept + x_coeff * data['x'],sigma=sigma, observed=data['y'])
    return model


prior_params = {
    'sigma beta':10,
    'sigma testval':1.,
    'intercept mu':0,
    'intercept sigma':20,
    'x mu':0,
    'x sigma':20,
}

create_app(model_method, data, **prior_params)