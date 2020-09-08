import pymc3 as pm
from prior_comparison_tool.main import create_app
import pandas as pd
from prior_comparison_tool.model import model
from prior_comparison_tool.plots import prior_density_plot, posterior_density_plot
import unittest
import timeit


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


class testCacheingAlgorithms(unittest.TestCase):

    model = model(model=model_method, data = data, model_kwargs=params)
    test_dict = {'model1':model}

    def test_individual_plot_cache_prior(self):
        """ A test for checking the add meal view when submitting valid data """
        time1 = timeit.timeit(prior_density_plot(variable='mu', data=self.test_dict, plottype='Separate Plots'), number=1)
        time2 = timeit.timeit(prior_density_plot(variable='mu', data=self.test_dict, plottype='Separate Plots'), number=1)
        self.assertLess(time1, time2, "The cache for individual prior density plot has not improved call time")

if __name__ == '__main__':
    unittest.main()