from prior_evaluation_tool.model import model
from prior_evaluation_tool.model_container import modelContainer
from prior_evaluation_tool.display_container_interaction import displayContainerInteraction
import pandas as pd
import itertools
import threading
import time
import sys

done = False

def animate():
    """animation for terminal output to say that the app is being created
        reassures user that something is happening and there is not just a 
        blank output"""
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rCreating App ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r\n')
    sys.stdout.flush()



def create_app(model_method, data, prior_kwargs:dict, InferenceData_dims={}, InferenceData_coords={}, num_samples_pymc3=1000):
    """
    function for creating the Prior Evaluation Tool
    returns the server already started

    @params
    model_method = the method for the pymc3 model (must take params data and prior kwargs and return pymc3 model instantiated)
    data = data for the model_method. A pandas dataframe or series object, will throw TypeError if not
    prior_kwargs = dict of the prior paramters. Used for the model_method
    
    **Optional Params
    num_samples_pymc3 = default(1000). Number of MCMC samples in pymc3. Only increase if necessary will increase app creation time
    InferenceData_dims = dict of dims for ArviZ InferenceData object
    InferenceData_coords = dict of coords for ArviZ InferenceData object
    """
    if not isinstance(data, pd.DataFrame or isinstance(data, pd.Series)):
        raise TypeError("Only Pandas DataFrame or Series allowed")
    else:
        # *** creates loading animation in console so user knows app is being created
        thread = threading.Thread(target=animate)
        thread.start()
        start_model = model(
            model=model_method, 
            data=data, 
            model_kwargs=prior_kwargs, 
            name='Original',
            InferenceData_dims=InferenceData_dims,
            InferenceData_coords=InferenceData_coords,
            num_samples_pymc3=num_samples_pymc3,
            )
        controls = displayContainerInteraction(start_model)
        # sets global var done to true to stop loading animation
        global done
        done = True
        return controls.app.start_server()
