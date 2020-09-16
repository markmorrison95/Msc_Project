import pymc3 as pm
from prior_evaluation_tool.main import create_app
import pandas as pd
from prior_evaluation_tool.model import model
import numpy as np

# ********** model taken from statistical rethinking - McElreath 2015 *************
def model_method(data, **prior_params):
    """
    Method for creating the PyMC3 model. 
    Parameters must be as represented. 
    Should return instantiated model
    """
    weight_m = np.vstack((data.weight_std, data.weight_std**2, data.weight_std**3))
    with pm.Model() as model:
        alpha = pm.Normal('alpha', mu=prior_params['alpha mu'], sd=prior_params['alpha sd'])
        beta = pm.Normal('beta', mu=prior_params['beta mu'], sd=prior_params['beta sd'], shape=3)
        sigma = pm.Uniform('sigma', lower=prior_params['sigma lower'], upper=prior_params['sigma upper'])
        mu = pm.Deterministic('mu', alpha + pm.math.dot(beta, weight_m))
        height = pm.Normal('height', mu=mu, sd=sigma, observed=data.height)
    return model


# data for the model
height_data = pd.read_csv("Howell1.csv", sep=";", header=0)
height_data = height_data[height_data.age >= 18]
height_data["weight_std"] = (height_data.weight - height_data.weight.mean()) / height_data.weight.std()

# Prior Paramaters for the model. Names should be understandable as used in program
params= {
    'alpha mu':178,
    'alpha sd':100,
    'beta mu':0,
    'beta sd':10,
    'sigma lower':0,
    'sigma upper':50,
}

# single method call for instantiating the Prior Evaluation Tool
create_app(
        model_method=model_method, 
        data=height_data, 
        prior_kwargs=params
        )