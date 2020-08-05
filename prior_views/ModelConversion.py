import arviz as az
import pymc3 as pm

def convert_models(models=[]):
    model_data = {}
    i = 1
    for m in models:
        with m:
            trace = pm.sample(1000)
            prior = pm.sample_prior_predictive(1000)
            posterior = pm.sample_posterior_predictive(trace)
            data = az.from_pymc3(
                        trace=trace,
                        prior=prior,
                        posterior_predictive=posterior,
                    )
            name = "prior_" + str(i) 
            i+=1
            model_data.update({name :data})
    return model_data