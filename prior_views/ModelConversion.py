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
        data = az.from_pymc3(
                    trace=trace,
                    posterior_predictive=posterior,
                )
    return data


def data_reduce_with_nan(data, fraction):
    """
    Reduces data by selecting random rows in the data series and then replacing them with
    numpy nan values. This is necessary when the number of data points is important, such
    as when they represent constant intervals in time.

    Throws type error if pandas dataframe of dataseries not used. 
    """
    if isinstance(data, pd.DataFrame) or isinstance(data, pd.Series):
        size = len(data)
        to_remove = int(size - (size*fraction))
        data.loc[list(data.loc[random.sample(list(data.index), to_remove)].index)] = np.nan
        return data
    else:
        raise TypeError("Only Pandas DataFrame or Series allowed")


def reduce_data_remove(data, fraction):
    """
    Reduces data by selecting random rows in the DataFrame and removing them entirely.
    Often replacing with nan values is not appropriate and will result in a model that 
    cannot be sampled from properly 

    Throws type error if pandas dataframe of dataseries not used. 
    """
    if isinstance(data, pd.DataFrame or isinstance(data, pd.Series)):
        size = len(data)
        to_remove = int(size - (size*fraction))
        data.drop(list(data.loc[random.sample(list(data.index), to_remove)].index))
        return data
    else:
        raise TypeError("Only Pandas DataFrame or Series allowed")



# def convert_models(models=[]):
#     model_data = {}
#     i = 1
#     for m in models:
#         with m:
#             trace = pm.sample(1000)
#             prior = pm.sample_prior_predictive(1000)
#             posterior = pm.sample_posterior_predictive(trace)
#             data = az.from_pymc3(
#                         trace=trace,
#                         prior=prior,
#                         posterior_predictive=posterior,
#                     )
#             name = "prior_" + str(i) 
#             i+=1
#             model_data.update({name :data})
#     return model_data