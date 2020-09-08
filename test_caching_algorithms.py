import pymc3 as pm
from prior_comparison_tool.main import create_app
import pandas as pd
from prior_comparison_tool.model import model
from prior_comparison_tool.plots import prior_density_plot, posterior_density_plot, posterior_predictive_density_plot, prior_predictive_density_plot
import unittest
import timeit
import numpy as np

RANDOM_SEED = 8927
np.random.seed(RANDOM_SEED)

# True parameter values
alpha, sigma = 1, 1
beta = [1, 2.5]
# Size of dataset
size = 100
# Predictor variable
X1 = np.random.randn(size)
X2 = np.random.randn(size) * 0.2
# Simulate outcome variable
Y = alpha + beta[0] * X1 + beta[1] * X2 + np.random.randn(size) * sigma
data = pd.Series(Y)

data = pd.DataFrame()
data['Y'] = Y
data['X1'] = X1
data['X2'] = X2



def model_method(data, **prior_params):
    with pm.Model() as test_model:

        # Priors for unknown model parameters
        alpha = pm.Normal("alpha", mu=prior_params['alpha mu'], sigma=prior_params['alpha sigma'])
        beta = pm.Normal("beta", mu=prior_params['beta mu'], sigma=prior_params['beta sigma'], shape=2)
        sigma = pm.HalfNormal("sigma", sigma=prior_params['sigma sigma'])

        # Expected value of outcome
        mu = alpha + beta[0] * data['X1'] + beta[1] * data['X2']

        # Likelihood (sampling distribution) of observations
        Y_obs = pm.Normal("Y_obs", mu=mu, sigma=sigma, observed=data['Y'])

    return test_model

params= {
    'alpha mu':0,
    'alpha sigma':10,
    'beta mu':0,
    'beta sigma':10,
    'sigma sigma':1,
}
params2= {
    'alpha mu':5,
    'alpha sigma':10,
    'beta mu':5,
    'beta sigma':10,
    'sigma sigma':1,
}


class testCacheingAlgorithms(unittest.TestCase):

    model1 = model(model=model_method, data = data, model_kwargs=params)
    model2 = model(model=model_method, data = data, model_kwargs=params2)
    test_dict_one_model = {'model1':model1}
    test_dict_two_models = {'model1':model1, 'model2':model2}

    def test_individual_plot_cache_prior(self):
        """ A test for checking that the cacheing of individual plots on prior works """
        def prior_funtion_call():
            return prior_density_plot(variable='alpha', data=self.test_dict_one_model, plottype='Separate Plots')

        time1 = timeit.timeit(prior_funtion_call, number=1)
        time2 = timeit.timeit(prior_funtion_call, number=1)
        self.assertLess(time2, time1, "The cache for individual prior density plot  - type: separate plot - has not improved call time")

        def prior_funtion_same_plot_call():
            return prior_density_plot(variable='alpha', data=self.test_dict_one_model, plottype='Same Plot')

        time1same = timeit.timeit(prior_funtion_same_plot_call, number=1)
        time2same = timeit.timeit(prior_funtion_same_plot_call, number=1)
        self.assertLess(time2same, time1same, "The cache for individual prior density plot - type: same plot - has not improved call time")

    def test_individual_plot_cache_posterior(self):
        """ A test for checking that the cacheing of individual plots on posterior works """
        def posterior_funtion_call():
            return posterior_density_plot(variable='alpha', data=self.test_dict_one_model, plottype='Separate Plots', percent=100)

        time1 = timeit.timeit(posterior_funtion_call, number=1)
        time2 = timeit.timeit(posterior_funtion_call, number=1)
        self.assertLess(time2, time1, "The cache for individual posterior density plot - type: separate plot - has not improved call time")

        def posterior_funtion_same_plot_call():
            return posterior_density_plot(variable='alpha', data=self.test_dict_one_model, plottype='Same Plots', percent=100)

        time1same = timeit.timeit(posterior_funtion_call, number=1)
        time2same = timeit.timeit(posterior_funtion_call, number=1)
        self.assertLess(time2same, time1same, "The cache for individual posterior density plot - type: same plot -  has not improved call time")


    def test_individual_plot_cache_posterior_ppc(self):
        """ A test for checking that the cacheing of individual plots on posterior ppc works """
        def posterior_ppc_funtion_call():
            return posterior_predictive_density_plot(variable='Y_obs', data=self.test_dict_one_model, percent=100)
        time1 = timeit.timeit(posterior_ppc_funtion_call, number=1)
        time2 = timeit.timeit(posterior_ppc_funtion_call, number=1)
        self.assertLess(time2, time1, "The cache for individual posterior ppc plot has not improved call time")

    def test_individual_plot_cache_prior_ppc(self):
        """ A test for checking that the cacheing of individual plots on prior ppc works """
        def prior_ppc_funtion_call():
            return prior_predictive_density_plot(variable='Y_obs', data=self.test_dict_one_model)
        time1 = timeit.timeit(prior_ppc_funtion_call, number=1)
        time2 = timeit.timeit(prior_ppc_funtion_call, number=1)
        self.assertLess(time2, time1, "The cache for individual prior ppc plot has not improved call time")

    def test_multiple_plot_cache_prior(self):
        """ A test for checking that the caching of multiple plots on prior works """
        def prior_funtion_call():
            return prior_density_plot(variable='alpha', data=self.test_dict_two_models , plottype='Separate Plots')

        time1 = timeit.timeit(prior_funtion_call, number=1)
        time2 = timeit.timeit(prior_funtion_call, number=1)
        self.assertLess(time2, time1, "The cache for multiple prior density plot  - type: separate plot - has not improved call time")

        def prior_funtion_same_plot_call():
            return prior_density_plot(variable='alpha', data=self.test_dict_two_models, plottype='Same Plot')

        time1same = timeit.timeit(prior_funtion_same_plot_call, number=1)
        time2same = timeit.timeit(prior_funtion_same_plot_call, number=1)
        self.assertLess(time2same, time1same, "The cache for multiple prior density plot - type: same plot - has not improved call time")


    def test_multiple_plot_cache_posterior(self):
        """ A test for checking that the cacheing of multiple plots on posterior works """
        def posterior_funtion_call():
            return posterior_density_plot(variable='alpha', data=self.test_dict_two_models, plottype='Separate Plots', percent=100)

        time1 = timeit.timeit(posterior_funtion_call, number=1)
        time2 = timeit.timeit(posterior_funtion_call, number=1)
        self.assertLess(time2, time1, "The cache for multiple posterior density plot - type: separate plot - has not improved call time")

        def posterior_funtion_same_plot_call():
            return posterior_density_plot(variable='alpha', data=self.test_dict_two_models, plottype='Same Plots', percent=100)

        time1same = timeit.timeit(posterior_funtion_call, number=1)
        time2same = timeit.timeit(posterior_funtion_call, number=1)
        self.assertLess(time2same, time1same, "The cache for multiple posterior density plot - type: same plot -  has not improved call time")


suite = unittest.TestLoader().loadTestsFromTestCase(testCacheingAlgorithms)
unittest.TextTestRunner(verbosity=2).run(suite)