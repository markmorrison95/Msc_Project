from prior_evaluation_tool.model import model
import arviz as az

class modelContainer:
    def __init__(self, model:model):
        self.original_model = model
        self.models_dict = {model.name:model}
        self.model_data = model.original_data

    def add_model(self, prior_args:dict, name):
        i = 1
        temp_name = name
        while temp_name in self.models_dict:
        # checks if the name already exists. If so adds a (1) or another int until free slot created
            temp_name = name + '('+ str(i) + ')'
            i+=1
        name = temp_name
        new_model = model(
            model=self.original_model.model_function, 
            data=self.model_data, 
            model_kwargs=prior_args,
            name=name,
            num_samples_pymc3=self.original_model.num_samples_pymc3, 
            InferenceData_coords=self.original_model.InferenceData_coords, 
            InferenceData_dims=self.original_model.InferenceData_dims,
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

    def compare_waic(self):
        model_data = {}
        for key, value in self.models_dict.items():
            model_data[key] = value.model_arviz_data
        comp = az.compare(
            model_data, 
            ic='waic'
            )
        return comp
