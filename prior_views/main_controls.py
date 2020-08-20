from prior_views.models_container import model_container
from prior_views.CreateApp import CreateApp


class Main_controls:

    def __init__(self, model):
        self.models = model_container(model)
        self.app = CreateApp(controls=self, models=self.models)


    def add_new_model_config(self, prior_args:dict, name:str):
        new_model = self.models.add_model(
            prior_args=prior_args,
            name = name,
            )
        self.app.new_model_added(new_prior_model=new_model)