import bokeh as Bokeh
import panel as pn
import bokeh.plotting as bkp
from bokeh.models import Legend
from bokeh.layouts import column, row
import arviz as az
from bokeh.document import without_document_lock
import sys



def prior_same_plot_list_cache(func):
    """
    Caches the list of the prior values created to allow the different model configs
    to be plotted on the same fig.
    Marginal gains, altough should be useful as more prior configs added
    """
    cache = {}
    def wrapped(model_dict):
        args = str(len(model_dict))
        if args in cache:
            return cache[args]
        else:
            val = func(model_dict)
            cache[args] = val
            return val
    return wrapped

@prior_same_plot_list_cache
def priors_same_plot_list(model_dict):
    data_list = []
    for model in model_dict.values():
        data_list.append(model.model_arviz_data)
    return data_list

def posterior_same_plot_list_cache(func):
    """
    Caches the list of the posterior values created based of the percentage request
    Marginal gains, altough may be useful as more prior configs added
    """
    cache = {}
    def wrapped(model_dict, percent):
        args = str(model_dict.keys()) + str(percent)
        if args in cache:
            return cache[args]
        else:
            val = func(model_dict, percent)
            cache[args] = val
            return val
    return wrapped

@posterior_same_plot_list_cache
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

def plot_cache(func):
    """
    Caching for the plots. Use the length of the dict of models (Data) to
    check if it is the same data being used as the dict is only added too not
    removed from. Saves checking if full dict is the same. Creates a string with length
    of dict and the other variable values to use as a key in dict to save return values

    *** if functionality for removing data is added will need to change *** 
    """
    cache = {}
    def wrapped(**kwargs):
        args = str(len(kwargs['data']))
        for k in kwargs.values():
            args += str(k)
        if args in cache:
            return cache[args]
        else:
            val = func(**kwargs)
            cache[args] = val
            return val
    return wrapped


@without_document_lock
@plot_cache
def prior_density_plot(variable, data, plottype, plot='prior'):
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
                if p.legend:
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




@without_document_lock
@plot_cache
def posterior_density_plot(variable, data, percent, plottype, plot='posterior'):
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
                if p.legend:
                    p.legend.visible = False
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





@without_document_lock
@plot_cache
def prior_predictive_density_plot(variable, data, plot='prior_predictive'):
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





def posterior_predictive_density_cache(func):
    cache = {}
    def wrapped(variable, data):
        args = str(len(data)) + variable
        if args in cache:
            return cache[args]
        else:
            val = func(variable, data)
            cache[args] = val
            return val
    return wrapped


@without_document_lock
@plot_cache
def posterior_predictive_density_plot(variable, data, plot='posterior_predictive'):
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




@without_document_lock
@plot_cache
def sample_trace_plot(variable, data, plot='sample_trace'):
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
            if p.legend:
                p.legend.visible = False
            p.x_range = x_axes
            p.y_range = y_axes
        plots.append(row(plot[0].tolist(), sizing_mode='scale_both'))
    col = column(plots)
    return col