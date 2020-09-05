import pandas as pd
import pymc3 as pm
import matplotlib.pyplot as plt
import numpy as np
import arviz as az

def CreateModel():
    disaster_data = pd.Series([4, 5, 4, 0, 1, 4, 3, 4, 0, 6, 3, 3, 4, 0, 2, 6,
                            3, 3, 5, 4, 5, 3, 1, 4, 4, 1, 5, 5, 3, 4, 2, 5,
                            2, 2, 3, 4, 2, 1, 3, np.nan, 2, 1, 1, 1, 1, 3, 0, 0,
                            1, 0, 1, 1, 0, 0, 3, 1, 0, 3, 2, 2, 0, 1, 1, 1,
                            0, 1, 0, 1, 0, 0, 0, 2, 1, 0, 0, 0, 1, 1, 0, 2,
                            3, 3, 1, np.nan, 2, 1, 1, 1, 1, 2, 4, 2, 0, 0, 1, 4,
                            0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1])
    years = np.arange(1851, 1962)

    with pm.Model() as disaster_model:
        switchpoint = pm.DiscreteUniform('switchpoint', lower=years.min(), upper = years.max(),testval=1900)



        early_rate = pm.Exponential('early_rate', 1)
        late_rate = pm.Exponential('late_rate', 1)

        rate = pm.math.switch(switchpoint >= years, early_rate, late_rate)

        disasters = pm.Poisson('disasters', rate, observed=disaster_data)

        trace = pm.sample(1000)
        prior = pm.sample_prior_predictive(1000)
        posterior = pm.sample_posterior_predictive(trace)

        pm_data = az.from_pymc3(
                trace=trace,
                prior=prior,
                posterior_predictive=posterior,
        )
        return pm_data