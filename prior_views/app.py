from prior_views.model import model
from prior_views.models_container import model_container
from prior_views.main_controls import Main_controls
import pandas as pd
import itertools
import threading
import time
import sys

done = False
# animation for terminal output to say that the app is being created
# reassures user that something is happening and there is not just a 
# blank output
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rCreating App ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r\n')



def app_view(model_method, data, **prior_kwargs):
    if not isinstance(data, pd.DataFrame or isinstance(data, pd.Series)):
        raise TypeError("Only Pandas DataFrame or Series allowed")
    else:
        thread = threading.Thread(target=animate)
        thread.start()
        start_model = model(model_method, data, prior_kwargs, name='Original')
        controls = Main_controls(start_model)
        global done
        done = True
        return controls.app.prior_checking_tool()
