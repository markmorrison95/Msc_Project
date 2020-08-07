import bokeh as Bokeh
import bokeh.plotting as bkp
from bokeh.models import Div
from bokeh.layouts import column, row
from bokeh.io import curdoc
import arviz as az
from functools import lru_cache
import functools
from theano.misc.frozendict import frozendict

def freezeargs(func):
    """Transform mutable dictionnary
    Into immutable
    Useful to be compatible with cache
    """
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        args = tuple([frozendict(arg) if isinstance(arg, dict) else arg for arg in args])
        kwargs = {k: frozendict(v) if isinstance(v, dict) else v for k, v in kwargs.items()}
        return func(*args, **kwargs)
    return wrapped


@freezeargs
@lru_cache(maxsize=32)
def prior_density_plot(variable,data, plottype='Seperate Plots'):
    """
    Method for producing the prior kde plot using arviz plot_density. This is done 2 ways: either will produce all     the plots onto one graph or will produe them seperately

    The parameters are the data, plottype, either "Seperate Plots" or "Same Plots" 

    Also takes the variable to view which will be chosen by the dropdown in the program. Probably shouldnt be          hardcoded with a default as this will change with each model.  *** Will change later ***
    """
    if plottype == 'Seperate Plots':
        plots = []
        for key, value in data.items():
            kwg = dict(title=key)
            curdoc().theme = 'dark_minimal'
            plot = az.plot_density(
                value,
                group='prior', 
                var_names=variable,
                outline=False, 
                backend='bokeh',
                shade=.5, 
                show=False,
                backend_kwargs=kwg,
                )
            for p in plot[0]:
                p.title.text = key+' '+p.title.text 
            plots.append(row(plot[0].tolist(), sizing_mode='scale_both'))
        col = column(plots)
    else:
        curdoc().theme = 'dark_minimal'
        plot = az.plot_density(
            list(data.values()), 
            group='prior', 
            var_names=variable,
            outline=False,  
            backend='bokeh',
            shade=.5, 
            show=False, 
            colors='cycle',
            data_labels=list(data.keys()),
            )
        col = column(plot[0].tolist())
    return col


@freezeargs
@lru_cache(maxsize=32)
def posterior_density_plot(variable, data, plottype):
    """
    Basically the sama as the prior density plot but uses the posterior instead. Could have resused the same           method with an extra param but the panel.interact method tries to create features for parameter selection          which i dont want in this case

    *** will try to find a workaround for this feature to reduce unnescesary code copying***
    """
    if plottype == 'Seperate Plots':
        plots = []
        for key,value in data.items():
            curdoc().theme = 'dark_minimal'
            kwg = dict(title=key)
            plot = az.plot_density(
                value, 
                group='posterior', 
                var_names=variable, 
                backend='bokeh',
                outline=False,
                shade=.5, 
                show=False,
                backend_kwargs=kwg
                )
            for p in plot[0]:
                p.title.text = key+' '+p.title.text 
            plots.append(row(plot[0].tolist(), sizing_mode='scale_both'))
        col = column(plots)
    else:
        curdoc().theme = 'dark_minimal'
        plot = az.plot_density(
            list(data.values()), 
            group='posterior', 
            var_names=variable, 
            backend='bokeh',
            shade=.5, 
            show=False, 
            colors='cycle',
            outline=False,
            data_labels=list(data.keys()),
            )
        col = column(plot[0].tolist())
    return col


def prior_predictive_density_plot(variable, data):
    plots = []
    for key, value in data.items():
        kwg = dict(title=key)
        curdoc().theme = 'dark_minimal'
        plot = az.plot_ppc(
            value, 
            group='prior', 
            var_names=variable, 
            backend='bokeh',
            alpha=.5, 
            show=False,
            backend_kwargs=kwg
            )
        plots.append(row(plot[0].tolist(), sizing_mode='scale_both'))
    col = column(plots)
    return col

def posterior_predictive_density_plot(variable, data):
    plots = []
    for key, value in data.items():
        kwg = dict(title=key)
        curdoc().theme = 'dark_minimal'
        plot = az.plot_ppc(
            value, 
            group='posterior', 
            var_names=variable, 
            backend='bokeh',
            alpha=.5, 
            show=False,
            backend_kwargs=kwg
            )
        for p in plot[0]:
            p.title.text = key+' '+p.title.text 
        plots.append(row(plot[0].tolist(), sizing_mode='scale_both'))
    col = column(plots)
    return col


@freezeargs
@lru_cache(maxsize=32)
def sample_trace_plot(variable, data):
    plots = []
    for key, value in data.items():
        kwg = dict(height=200,title=key)
        curdoc().theme = 'dark_minimal'
        plot = az.plot_trace(
            value, 
            var_names=variable, 
            backend='bokeh', 
            show=False,
            backend_kwargs=kwg,
            compact=True,
            combined=True,
            )
        for p in plot[0]:
            p.title.text = key+' '+p.title.text 
        plots.append(row(plot[0].tolist(), sizing_mode='scale_both'))
    col = column(plots)
    return col