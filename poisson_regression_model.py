import numpy as np
import pandas as pd
import seaborn as sns
import patsy as pt
import pymc3 as pm
from prior_comparison_tool.main import create_app


theta_noalcohol_meds = 1    # no alcohol, took an antihist
theta_alcohol_meds = 3      # alcohol, took an antihist
theta_noalcohol_nomeds = 6  # no alcohol, no antihist
theta_alcohol_nomeds = 36   # alcohol, no antihist

# create samples
q = 1000
df = pd.DataFrame({
        'nsneeze': np.concatenate((np.random.poisson(theta_noalcohol_meds, q),
                                   np.random.poisson(theta_alcohol_meds, q),
                                   np.random.poisson(theta_noalcohol_nomeds, q),
                                   np.random.poisson(theta_alcohol_nomeds, q))),
        'alcohol': np.concatenate((np.repeat(False, q),
                                   np.repeat(True, q),
                                   np.repeat(False, q),
                                   np.repeat(True, q))),
        'nomeds': np.concatenate((np.repeat(False, q),
                                      np.repeat(False, q),
                                      np.repeat(True, q),
                                      np.repeat(True, q)))})

fml = fml = 'nsneeze ~ alcohol * nomeds'
(mx_en, mx_ex) = pt.dmatrices(fml, df, return_type='dataframe', NA_action='raise')
pd.concat((mx_ex.head(3),mx_ex.tail(3)))
data = pd.DataFrame(mx_ex)
data['nsneeze'] = mx_en['nsneeze']

def model_method(data, **prior_kwargs):

    with pm.Model() as mdl_fish:

        # define priors, weakly informative Normal
        b0 = pm.Normal('b0_intercept', mu=prior_kwargs['b0_intercept_mu'], sigma=prior_kwargs['b0_intercept sigma'])
        b1 = pm.Normal('b1_alcohol[T.True]', mu=prior_kwargs['b1_alcohol[T.True]_mu'], sigma=prior_kwargs['b1_alcohol[T.True]_sigma'])
        b2 = pm.Normal('b2_nomeds[T.True]', mu=prior_kwargs['b2_nomeds[T.True]_mu'], sigma=prior_kwargs['b2_nomeds[T.True]_sigma'])
        b3 = pm.Normal('b3_alcohol[T.True]:nomeds[T.True]', mu=prior_kwargs['b3_alcohol[T.True]:nomeds[T.True]_mu'], sigma=prior_kwargs['b3_alcohol[T.True]:nomeds[T.True]_sigma'])

        # define linear model and exp link function
        theta = (b0 +
                b1 * data['alcohol[T.True]'] +
                b2 * data['nomeds[T.True]'] +
                b3 * data['alcohol[T.True]:nomeds[T.True]'])

        ## Define Poisson likelihood
        y = pm.Poisson('y', mu=np.exp(theta), observed=data['nsneeze'])
        print(np.exp(theta))

    return mdl_fish



prior_params = {
            'b0_intercept_mu' :0,
            'b1_alcohol[T.True]_mu':0,
            'b2_nomeds[T.True]_mu':0,
            'b3_alcohol[T.True]:nomeds[T.True]_mu':0,
            'b0_intercept sigma':10,
            'b1_alcohol[T.True]_sigma':10,
            'b2_nomeds[T.True]_sigma':10,
            'b3_alcohol[T.True]:nomeds[T.True]_sigma' :10,
            }

mod = model_method( data, **prior_params)

with mod:
    pm.sample_prior_predictive(250, var_names='y')
