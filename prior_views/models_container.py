from prior_views.model import model
import webbrowser

class model_container:
    def __init__(self, model:model):
        self.original_model = model
        self.models_dict = {model.name:model}
        self.model_data = model.original_data

    def add_model(self, prior_args:dict, name):
        new_model = model(
            model=self.original_model.model_function, 
            data=self.model_data, 
            model_kwargs=prior_args,
            name=name
            )
        self.models_dict[name] = new_model
        return new_model
    
    def arviz_data_list(self):
        data = []
        for m in self.models_dict.values():
            data.append(m.model_arviz_data)
        return data

    def prior_variables(self):
        return self.original_model.prior_variables()

    def posterior_variables(self):
        return self.original_model.posterior_variables()
