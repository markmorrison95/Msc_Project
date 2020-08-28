from prior_views.model import model
from prior_views.models_container import model_container
from prior_views.main_controls import Main_controls
import itertools
import threading
import time
import sys

done = False
#here is the animation
def loading_animation():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rCreating App ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r')



def app_view(model_method, data, **prior_kwargs):
    t = threading.Thread(target=loading_animation)
    t.start()
    start_model = model(model_method, data, prior_kwargs, name='Original')
    controls = Main_controls(start_model)
    global done
    done = True
    return controls.app.prior_checking_tool()
