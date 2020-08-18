from prior_views.models_container import model_container
from prior_views.CreateApp import CreateApp


class Main_controls:

    def __init__(self, model):
        self.models = model_container(model)
        self.app = CreateApp(controls=self, models=self.models)


    def add_new_model_config(self, prior_args:dict):
        models.add_model(prior_args=prior_args)
        self.app.new_model_added()