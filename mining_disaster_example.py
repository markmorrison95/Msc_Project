import pandas as pd
import pymc3 as pm
import matplotlib.pyplot as plt
import numpy as np
from prior_evaluation_tool.main import create_app

disaster_data = pd.Series([4, 5, 4, 0, 1, 4, 3, 4, 0, 6, 3, 3, 4, 0, 2, 6,
                           3, 3, 5, 4, 5, 3, 1, 4, 4, 1, 5, 5, 3, 4, 2, 5,
                           2, 2, 3, 4, 2, 1, 3, np.nan, 2, 1, 1, 1, 1, 3, 0, 0,
                           1, 0, 1, 1, 0, 0, 3, 1, 0, 3, 2, 2, 0, 1, 1, 1,
                           0, 1, 0, 1, 0, 0, 0, 2, 1, 0, 0, 0, 1, 1, 0, 2,
                           3, 3, 1, np.nan, 2, 1, 1, 1, 1, 2, 4, 2, 0, 0, 1, 4,
                           0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1], dtype='float64')

years = np.arange(1851, 1962)
disaster_data = disaster_data.to_frame()
disaster_data['year'] = years

m_kwars = dict(early_rate_lambda=1, late_rate_lambda=1)

def model_method(data, **kwargs):
    with pm.Model() as disaster_model:
        switchpoint = pm.DiscreteUniform('switchpoint', lower=disaster_data['year'].min(), upper = disaster_data['year'].max(), testval=disaster_data['year'].median())

        early_rate = pm.Exponential('early_rate', m_kwars['early_rate_lambda'])
        late_rate = pm.Exponential('late_rate', m_kwars['late_rate_lambda'])

        rate = pm.math.switch(switchpoint >= disaster_data['year'], early_rate, late_rate)

        disasters = pm.Poisson('disasters', rate, observed=disaster_data[0])

    return disaster_model


create_app(
        model_method=model_method, 
        data=disaster_data, 
        prior_kwargs=m_kwars,
        )