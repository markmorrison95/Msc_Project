import PriorViews.Tabs
import PriorViews.Plots
import PriorViews.ViewConstructor as vc

class ModelConversion:

    def __init__(self, models=[]):
        self.models = models
        data = convert_models()
        plots = Plots(models=data)
        tabs = Tabs(model=data,plots=plots)
        view = vc.final_view(tabs=tabs)


    def convert_models(self, models=self.models):
        model_data = []
        for m in models:
            with m:
                data = az.from_pymc3(
                            trace=trace,
                            prior=prior,
                            posterior_predictive=posterior,
                        )
                model_data.append(data)
        return model_data