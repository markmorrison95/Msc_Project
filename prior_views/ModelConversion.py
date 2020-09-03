import arviz as az
import pymc3 as pm
import random
import numpy as np
import pandas as pd

import logging

# removes pymc3 sampling output apart from errors
logger = logging.getLogger('pymc3')
logger.setLevel(logging.ERROR)

def convert_full_model(model):
    with model:
        trace = pm.sample(progressbar=False)
        prior = pm.sample_prior_predictive()
        posterior = pm.sample_posterior_predictive(trace,progressbar=False)
        """********************************************************
            Forcing the output values from the model to be
            float64. This creates continuity on the values
            and allows for plotting of multiple variables/outputs
            into one plot without error"""
        for key, val in prior.items():
                prior[key] = val.astype('float64')
        for key, val in posterior.items():
            posterior[key] = val.astype('float64')
        """*******************************************************"""
        data = az.from_pymc3(
                    trace=trace,
                    prior=prior,
                    posterior_predictive=posterior,
                )
    return data

def convert_posterior_model(model):
    with model:
        trace = pm.sample(progressbar=False)
        posterior = pm.sample_posterior_predictive(trace,progressbar=False)
        """********************************************************
            Forcing the output values from the model to be
            float64. This creates continuity on the values
            and allows for plotting of multiple variables/outputs
            into one plot without error"""
        for key, val in posterior.items():
            posterior[key] = val.astype('float64')
        """*******************************************************"""
        data = az.from_pymc3(
                    trace=trace,
                    posterior_predictive=posterior,
                )
    return data



def reduce_data_remove(data, fraction):
    """
    Reduces data by selecting random rows in the DataFrame and removing them entirely.
    Often replacing with nan values is not appropriate and will result in a model that 
    cannot be sampled from properly 

    Throws type error if pandas dataframe of dataseries not used. 
    """
    if isinstance(data, pd.DataFrame or isinstance(data, pd.Series)):
        data = data.copy(deep=True)
        size = len(data)
        to_remove = int(size - (size*fraction))
        data = data.drop(list(data.loc[random.sample(list(data.index), to_remove)].index))
        return data
    else:
        raise TypeError("Only Pandas DataFrame or Series allowed")
