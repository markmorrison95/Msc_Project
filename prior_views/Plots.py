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
    to be plotted on the same figure.
    Marginal gains, although should be useful as more prior configs added
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


def individual_plot_cache(func):
    """
    function decorator used for cacheing individual plots. Same method used for all plot types. 
    Stores based on group, key (model config name) and variable combinations. These should be unique for the given plots in all cases
    apart from posterior KDE. 
    
    In that case:
        Checks if the kwargs contains a percent. The original key will have percent added to define the plot.
    """
    cache = {}
    def wrapped(**kwargs):
        cache_key = str(kwargs['group'] + kwargs['key'] + kwargs['var'])
        if 'percent' in kwargs:
            cache_key += str(kwargs['percent'])
        if cache_key in cache:
            return cache[cache_key]
        else:
            val = func(**kwargs)
            cache[cache_key] = val
            return val
    return wrapped

# *************** function for creating KDE plots *******************************
@individual_plot_cache
def plot_call_KDE(group, key, var, value, percent=100):
    """ using seperated function to allow for plot caching. Used for both prior and posterior
    KDE plots. If the key, var combo has already been called for that group the plot 
    will be retrieved from cache.
    
    @group should be either prior or posterior 
    
    if the group is posterior will check the percentage of data it needs to plot
    """

    if group == 'posterior':
        data = value.posteriors[percent]
    else:
        data = value.model_arviz_data
    kwg = dict(height=250, width=550)
    plot = az.plot_density(
        data,
        group=group, 
        var_names=var,
        outline=False, 
        backend='bokeh',
        shade=.5, 
        show=False,
        colors=value.color,
        backend_kwargs=kwg
        )
    for p in plot[0]:
        # setting the title of the plots so have the config name at the start
        # also changing the axis range so plots are linked at same range
        p.title.text = key+' '+p.title.text 
        if p.legend:
            p.legend.visible = False
    return plot
# ************************************************************************************


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
        x_axis_range, y_axis_range = [],[]

        for key, value in data.items():
            plot = plot_call_KDE(group='prior', key=key, var=variable, value=value)
            plots.append(row(plot[0].tolist()))
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
    This is done 2 ways: either will produce all the plots onto one graph or will produce them seperately
    The parameters are the data : dictionary of model objects, plottype, either "Separate Plots" or "Same Plots" 
    Also takes the variable to view which will be chosen by the dropdown in the program. Requires a percentage which translates
    to a percentage of data used. This corresponds to the values set in the model objects
    """
    if plottype == 'Separate Plots':
        plots = []
        kwg = dict(height=250, width=550)
        x_axis_range, y_axis_range = [],[]
        for key,value in data.items():
            plot = plot_call_KDE(group='posterior', key=key, var=variable, value=value, percent=percent)
            plots.append(row(plot[0].tolist()))
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


# *************** function for creating PPC plots *******************************
@individual_plot_cache
def plot_call_ppc(group, key, var, value, percent=100):
    """ using seperated function to allow for plot caching. Used for both prior and posterior
    KDE plots. If the key, var combo has already been called for that group the plot 
    will be retrieved from cache.
    
    @group should be either prior or posterior """
    if group == 'posterior':
        data = value.posterior_predictive[percent]
    else:
        data = value.model_arviz_data
    kwg = dict(height=350, width=500)
    # x_axis_range, y_axis_range = [],[]
    plot = az.plot_ppc(
        data, 
        group=group, 
        var_names=var, 
        backend='bokeh',
        alpha=.5, 
        show=False,
        backend_kwargs=kwg,
        num_pp_samples=250,
        legend=True,
    )
    for p in plot[0]:
        # setting the title of the plots so have the config name at the start
        # also changing the axis range so plots are linked at same range
        p.title.text = key+' '+p.title.text 
        # p.x_range = x_axes
        # p.y_range = y_axes
    return plot
# ************************************************************************************









@without_document_lock
@plot_cache
def prior_predictive_density_plot(variable, data, plot='prior_predictive'):
    plots = []
    kwg = dict(height=350, width=500)
    x_axis_range, y_axis_range = [],[]
    for key, value in data.items():
        plot = plot_call_ppc(group='prior', key=key, var=variable, value=value)
        plots.append(row(plot[0].tolist()))
    col = column(plots)
    return col






@without_document_lock
@plot_cache
def posterior_predictive_density_plot(variable, data, percent, plot='posterior_predictive',):
    plots = []
    x_axis_range, y_axis_range = [],[]
    kwg = dict(height=350, width=500)
    for key, value in data.items():
        plot = plot_call_ppc(group='posterior', key=key, var=variable, value=value, percent=percent)
        plots.append(row(plot[0].tolist()))
    col = column(plots)
    return col




# *************** function for creating Trace plots *******************************
@individual_plot_cache
def plot_call_trace(group, key, var, value):
    """ using seperated function to allow for plot caching. Used for both prior and posterior
    KDE plots. If the key, var combo has already been called for that group the plot 
    will be retrieved from cache.
    
    @group should be either prior or posterior """
    kwg = dict(height=200)
    plot = az.plot_trace(
        value.model_arviz_data, 
        var_names=var,
        backend='bokeh', 
        show=False,
        backend_kwargs=kwg,
        compact=True,
        combined=True,
        )
    for p in plot[0]:
        # setting the title of the plots so have the config name at the start
        # also changing the axis range so plots are linked at same range
        p.title.text = key+' '+p.title.text 
        if p.legend:
            p.legend.visible = False
    return plot
# ************************************************************************************


@without_document_lock
@plot_cache
def sample_trace_plot(variable, data, plot='sample_trace'):
    plots = []
    kwg = dict(height=200)
    x_axis_range, y_axis_range = [],[]
    for key, value in data.items():
        plot = plot_call_trace(group='', key=key, var=variable, value=value)
        plots.append(row(plot[0].tolist()))
    col = column(plots)
    return col



    