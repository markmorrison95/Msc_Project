import bokeh as Bokeh
import panel as pn
import bokeh.plotting as bkp
from bokeh.models import Legend
from bokeh.layouts import column, row
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
def priors_same_plot_list(model_dict):
    data_list = []
    for model in model_dict.values():
        data_list.append(model.model_arviz_data)
    return data_list

@freezeargs
@lru_cache(maxsize=32)
def posteriors_same_plot_list(model_dict, percent):
    data_list = []
    for model in model_dict.values():
        data_list.append(model.posteriors[percent])
    return data_list

def color_pool_gen(model_dict):
    colors = []
    for model in model_dict.values():
        colors.append(model.color)
    return colors


def prior_density_plot(variable,data, plottype='Separate Plots'):
    """
    Method for producing the prior kde plot using arviz plot_density. 
    This is done 2 ways: either will produce all the plots onto one graph or will produe them seperately
    The parameters are the data, plottype, either "Seperate Plots" or "Same Plots" 
    Also takes the variable to view which will be chosen by the dropdown in the program. 
    """
    if plottype == 'Separate Plots':
        plots = pn.Column(scroll=True, max_height=750, sizing_mode='stretch_both')
        kwg = dict(height=250, width=550)
        x_axis_range, y_axis_range = [],[]
        for key, value in data.items():
            plot = az.plot_density(
                value.model_arviz_data,
                group='prior', 
                var_names=variable,
                outline=False, 
                backend='bokeh',
                shade=.5, 
                show=False,
                colors=value.color,
                backend_kwargs=kwg
                )
            if len(x_axis_range) == 0:
                for p in plot[0]:
                    x_axis_range.append(p.x_range)
                    y_axis_range.append(p.y_range)
            for p, x_axes, y_axes in zip(plot[0], x_axis_range, y_axis_range):
                # setting the title of the plots so have the config name at the start
                # also changing the axis range so plots are linked at same range
                p.title.text = key+' '+p.title.text 
                p.legend.visible = False
                p.x_range = x_axes
                p.y_range = y_axes
            plots.append(row(plot[0].tolist(), sizing_mode='scale_both'))
        col = plots
    else:
        kwg = dict(height=450, width=650,toolbar_location='right')
        plot = az.plot_density(
            priors_same_plot_list(data), 
            group='prior', 
            var_names=variable,
            outline=False,  
            backend='bokeh',
            shade=.5, 
            show=False, 
            colors=color_pool_gen(data),
            data_labels=list(data.keys()),
            backend_kwargs=kwg,
            )
        for p in plot[0]:
            legend = p.legend[0]
            legend.location = (10,-10)
            legend.orientation = "vertical"
            p.add_layout(legend, place='right')
        col = column(plot[0].tolist())
    return col



def posterior_density_plot(variable, data, percent, plottype):
    """
    Method for producing the posterior kde plot using arviz plot_density. 
    This is done 2 ways: either will produce all the plots onto one graph or will produe them seperately
    The parameters are the data : dictionary of model objects, plottype, either "Separate Plots" or "Same Plots" 
    Also takes the variable to view which will be chosen by the dropdown in the program. Requires a percentage which translates
    to a percentage of data used. This corresponds to the values set in the model objects
    """
    if plottype == 'Separate Plots':
        plots = []
        kwg = dict(height=250, width=550)
        x_axis_range, y_axis_range = [],[]
        for key,value in data.items():
            plot = az.plot_density(
                value.posteriors[percent],
                group='posterior', 
                var_names=variable, 
                backend='bokeh',
                outline=False,
                shade=.5, 
                show=False,
                colors=value.color,
                backend_kwargs=kwg,
                )
        if len(x_axis_range) == 0:
            for p in plot[0]:
                x_axis_range.append(p.x_range)
                y_axis_range.append(p.y_range)
        for p, x_axes, y_axes in zip(plot[0], x_axis_range, y_axis_range):
            # setting the title of the plots so have the config name at the start
            # also changing the axis range so plots are linked at same range
            p.title.text = key+' '+p.title.text 
            p.x_range = x_axes
            p.y_range = y_axes
            plots.append(row(plot[0].tolist(), sizing_mode='scale_both'))
        col = column(plots)
    else:
        kwg = dict(height=450, width=650,toolbar_location='right')
        plot = az.plot_density(
            posteriors_same_plot_list(data, percent), 
            group='posterior', 
            var_names=variable, 
            backend='bokeh',
            shade=.5, 
            show=False, 
            colors=color_pool_gen(data),
            outline=False,
            data_labels=list(data.keys()),
            backend_kwargs=kwg,
            )
        for p in plot[0]:
            legend = p.legend[0]
            legend.location = (10,-10)
            legend.orientation = "vertical"
            p.add_layout(legend, place='right')
        col = column(plot[0].tolist())
    return col


def prior_predictive_density_plot(variable, data):
    plots = []
    kwg = dict(height=350, width=500)
    x_axis_range, y_axis_range = [],[]
    for key, value in data.items():
        plot = az.plot_ppc(
            value.model_arviz_data, 
            group='prior', 
            var_names=variable, 
            backend='bokeh',
            alpha=.5, 
            show=False,
            backend_kwargs=kwg,
            num_pp_samples=250,
        )
        if len(x_axis_range) == 0:
            for p in plot[0]:
                x_axis_range.append(p.x_range)
                y_axis_range.append(p.y_range)
        for p, x_axes, y_axes in zip(plot[0], x_axis_range, y_axis_range):
            # setting the title of the plots so have the config name at the start
            # also changing the axis range so plots are linked at same range
            p.title.text = key+' '+p.title.text 
            p.x_range = x_axes
            p.y_range = y_axes
        plots.append(row(plot[0].tolist(), sizing_mode='scale_both'))
    col = column(plots)
    return col

def posterior_predictive_density_plot(variable, data):
    plots = []
    x_axis_range, y_axis_range = [],[]
    kwg = dict(height=350, width=500)
    for key, value in data.items():
        plot = az.plot_ppc(
            value.model_arviz_data, 
            group='posterior', 
            var_names=variable, 
            backend='bokeh',
            alpha=.5, 
            show=False,
            backend_kwargs=kwg,
            # reduce the number of samples just to improve loading dows. Seems 
            # to slow down the whole application if samples plotted are too high
            num_pp_samples=250,
            )
        if len(x_axis_range) == 0:
            for p in plot[0]:
                x_axis_range.append(p.x_range)
                y_axis_range.append(p.y_range)
        for p, x_axes, y_axes in zip(plot[0], x_axis_range, y_axis_range):
            # setting the title of the plots so have the config name at the start
            # also changing the axis range so plots are linked at same range
            p.title.text = key+' '+p.title.text 
            p.x_range = x_axes
            p.y_range = y_axes
        plots.append(row(plot[0].tolist(), sizing_mode='scale_both'))
    col = column(plots)
    return col


def sample_trace_plot(variable, data):
    plots = []
    kwg = dict(height=200)
    x_axis_range, y_axis_range = [],[]
    for key, value in data.items():
        plot = az.plot_trace(
            value.model_arviz_data, 
            var_names=variable, 
            backend='bokeh', 
            show=False,
            backend_kwargs=kwg,
            compact=True,
            combined=True,
            )
        if len(x_axis_range) == 0:
            for p in plot[0]:
                x_axis_range.append(p.x_range)
                y_axis_range.append(p.y_range)
        for p, x_axes, y_axes in zip(plot[0], x_axis_range, y_axis_range):
            # setting the title of the plots so have the config name at the start
            # also changing the axis range so plots are linked at same range
            p.title.text = key+' '+p.title.text 
            p.legend.visible = False
            p.x_range = x_axes
            p.y_range = y_axes
        plots.append(row(plot[0].tolist(), sizing_mode='scale_both'))
    col = column(plots)
    return col