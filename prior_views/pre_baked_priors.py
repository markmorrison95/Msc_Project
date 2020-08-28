import pymc3 as pm 

default_priors = {}

# default_priors = {

# }



# pm.Normal.dist(0,10)
# pm.Normal.dist(0,100)
# pm.Normal.dist(-100,100)
# pm.Normal.dist(0,1)
# pm.Normal.dist(0,1/.001)
# pm.HalfNormal.dist(0,1)
# pm.InverseGamma.dist(1,100)
# pm.Gamma.dist(1.5, 10**-4)

class pre_made_prior():
    def __init__(self, distribution, description, **params):
        params_string = ''
        for key, val in params.items():
            params_string += key + ':'+ str(val) + ' '
        self.tag = description + ' (' + params_string +')'
        self.distribution = distribution
        self.params = params


normal_params_list = [[0,10],[0,100],[-100,100],[0,1],[0,1/.001]]
for params in normal_params_list:
    kw = {'mean':params[0],
            'SD':params[1]}
    prior = pre_made_prior(pm.Normal.dist,'Normal Distribution', **kw)
    default_priors[prior.tag] = prior