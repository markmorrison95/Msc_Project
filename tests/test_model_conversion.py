import unittest
import pandas as pd
import numpy as np
from prior_evaluation_tool.model_conversion import reduce_data_remove, convert_full_model, convert_posterior_model
import pymc3 as pm

RANDOM_SEED = 8927
np.random.seed(RANDOM_SEED)


# *********************** model taken from https://docs.pymc.io/notebooks/getting_started.html ******************
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
data_series= pd.Series(Y)

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

class testModelConversion(unittest.TestCase):
    """
    Class for testing hte methods from the modelConversion class. Ensures data is being created as expected
    as well as checking for consistency accross different config inputs
    """ 
    def test_data_removal_panda_series(self):
        """ Test that correct amount of data is being removed when using pandas series
        """
        reduced_data = reduce_data_remove(data=data_series,fraction=.5)
        self.assertAlmostEqual(len(reduced_data), (len(data_series)*.5))


    def test_data_removal_panda_DataFrame(self):
        """ Test that correct amount of data is being removed when using pandas DataFrame
        """
        reduced_data = reduce_data_remove(data=data,fraction=.5)
        self.assertAlmostEqual(len(reduced_data), (len(data)*.5))

    model1 = model_method(data, **params)
    model2 = model_method(data, **params2)
    data1 = convert_full_model(
            model=model1,
            num_samples=1000,
            InferenceData_coords={},
            InferenceData_dims={})
    data2 = convert_full_model(model2,
            num_samples=1000,
            InferenceData_coords={},
            InferenceData_dims={},
        )

    def test_sample_size_consistency(self):
        """ Test to ensure consistent MCMC sampling size across different model configs
        """
        self.assertEqual(len(self.data1.posterior.draw), len(self.data2.posterior.draw))

    def test_float_conversion(self):
        """
        Test to ensure that the conversion of values in prior and posterio to float64 is being completed and mantained into InferenceData object
        """
        for var in self.data1.posterior.data_vars:
            self.assertEqual(self.data1.posterior[var].dtype, 'float64', 'Value not being properly mantained as float64 in InferenceData object')
        for var in self.data1.prior.data_vars:
            self.assertEqual(self.data1.prior[var].dtype, 'float64', 'Value not being properly mantained as float64 in InferenceData object')


suite = unittest.TestLoader().loadTestsFromTestCase(testModelConversion)
unittest.TextTestRunner(verbosity=2).run(suite)