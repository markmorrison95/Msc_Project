import pymc3 as pm
from prior_views.app import app_view
import pandas as pd


def model_method(data, **prior_params):
    with pm.Model() as model:
        mu = pm.Normal("mu", mu=prior_params['height_mean_mu'], sd=prior_params['height_mean_sd'])
        sigma = pm.Uniform("sigma", lower=prior_params['sd_lower'], upper=prior_params['sd_upper'])
        height = pm.Normal("height", mu=mu, sd=sigma, observed=data.height)

    return model



d = pd.read_csv("Howell1.csv", sep=";", header=0)
data = d[d.age >= 18]

params= {
    'height_mean_mu':178,
    'height_mean_sd':20,
    'sd_lower':0,
    'sd_upper':50,
}



app = app_view(model_method, data, **params)