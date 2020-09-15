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
    """
    Runs MCMC sampling on model provided and creates data for prior, posterior and PPC
    packages data into ArviZ InferenceData object and returns that
    """
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
    """
    Runs MCMC sampling on model provided and creates data for posterior and PPC
    Does not produce prior data because not required
    packages data into ArviZ InferenceData object and returns that
    """
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




def data_reduce_cache(func):
    """
    caching the call to reduce the data so that the same reduced data set is 
    used for all models. Could have stored the data somewhere else but made the change at end
    and wanted to fix the issue without changing the rest of the program
    """
    cache = {}
    def wrapped(**kwargs):
        args = kwargs['fraction']
        if args in cache:
            return cache[args]
        else:
            val = func(**kwargs)
            cache[args] = val
            return val
    return wrapped


@data_reduce_cache
def reduce_data_remove(data, fraction):
    """
    Reduces data by selecting random rows in the DataFrame and removing them entirely.
    Often replacing with nan values is not appropriate and will result in a model that 
    cannot be sampled from properly 

    Throws type error if pandas dataframe of dataseries not used. 
    """
    if isinstance(data, pd.DataFrame) or isinstance(data, pd.Series):
        data = data.copy(deep=True)
        size = len(data)
        to_remove = int(size - (size*fraction))
        data = data.drop(list(data.loc[random.sample(list(data.index), to_remove)].index))
        return data
    else:
        raise TypeError("Only Pandas DataFrame or Series allowed")
