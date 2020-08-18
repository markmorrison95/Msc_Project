from prior_views.model import model
from prior_views.models_container import model_container
from prior_views.main_controls import Main_controls

def app_view(model_method, data, **prior_kwargs):
    start_model = model(model_method, data, prior_kwargs)
    controls = Main_controls(start_model)
    return controls.app.prior_checking_tool()

