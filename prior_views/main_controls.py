from prior_views.models_container import model_container
from prior_views.CreateApp import CreateApp
from pymc3.exceptions import SamplingError


class Main_controls:

    def __init__(self, model):
        self.models = model_container(model)
        self.app = CreateApp(controls=self, models=self.models)


    def add_new_model_config(self, prior_args:dict, name:str):
        try:
            new_model = self.models.add_model(
                prior_args=prior_args,
                name = name,
                )
            self.app.new_model_added(new_prior_model=new_model)
        except Exception:
            # catches any exception from constructing and sampling the model
            # not ideal. Would like to specify the error type and give a more informative
            # warning message but struggling with catching some custom pymc3 exceptions
            self.app.sampling_failed()