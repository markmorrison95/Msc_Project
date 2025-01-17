import bokeh as Bokeh
import panel as pn
import bokeh.plotting as bkp
from bokeh.models import Legend
from bokeh.layouts import column, row
import arviz as az
import numpy as np
from bokeh.models import LegendItem, Legend
from bokeh.document import without_document_lock
import copy
import logging

logger = logging.getLogger('arviz')
logger.setLevel(logging.ERROR)

def priors_same_plot_list(model_dict):
    """
    creates a list of all the model data so that it can be plotted on the one figure
    """
    data_list = []
    for model in model_dict.values():
        data_list.append(model.model_arviz_data)
    return data_list

def posteriors_same_plot_list(model_dict, percent):
    """
    creates a list of all the model data so that it can be plotted on the one figure
    does the same thing as prior but takes the percent into consideration 
    """
    data_list = []
    for model in model_dict.values():
        data_list.append(model.posteriors[percent])
    return data_list

def color_pool_gen(model_dict):
    """
    takes the dictionary of the model objects and creates a list of all the 
    colors associated with them. In python dictionary order is mantained so
    when creating the plots the colors will line up with the list
    """
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
        args += str(list(kwargs.values()))
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
    plots = pn.Column(scroll=True, max_height=750, sizing_mode='stretch_both')
    if plottype == 'Separate Plots':
        for key, value in data.items():
            plot = plot_call_KDE(group='prior', key=key, var=variable, value=value)
            plots.append(row(plot[0].tolist()))
    else:
        kwg = dict(height=450, width=650,toolbar_location='right')
        plot = az.plot_density(
            priors_same_plot_list(model_dict=data), 
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
            # move legend to side of plot so its not obscuring any info
            legend = p.legend[0]
            legend.location = (10,-10)
            legend.orientation = "vertical"
            p.add_layout(legend, place='right')
        plots.append(column(plot[0].tolist()))
    return plots




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

    plots = pn.Column(scroll=True, max_height=750, sizing_mode='stretch_both')
    if plottype == 'Separate Plots':
        kwg = dict(height=250, width=550)
        x_axis_range, y_axis_range = [],[]
        for key,value in data.items():
            plot = plot_call_KDE(group='posterior', key=key, var=variable, value=value, percent=percent)
            plots.append(row(plot[0].tolist()))
    else:
        kwg = dict(height=450, width=650,toolbar_location='right')
        plot = az.plot_density(
            posteriors_same_plot_list(model_dict=data, percent=percent), 
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
            # move legend to side of plot so its not obscuring any info
            legend = p.legend[0]
            legend.location = (10,-10)
            legend.orientation = "vertical"
            p.add_layout(legend, place='right')
        plots.append(column(plot[0].tolist()))
    return plots


# *************** function for creating PPC plots *******************************
@individual_plot_cache
def plot_call_ppc(group, key, var, value, percent=100):
    """ using seperated function to allow for plot caching. Used for both prior and posterior
    KDE plots. If the key, var combo has already been called for that group the plot 
    will be retrieved from cache.
    
    @group should be either prior or posterior """
    color = value.color
    if group == 'Posterior':
        data = value.posterior_predictive[percent]
    else:
        data = value.model_arviz_data
    kwg = dict(height=350, width=500)
    plot = az.plot_ppc(
        data, 
        group=group.lower(), 
        var_names=var, 
        backend='bokeh',
        alpha=.5, 
        show=False,
        backend_kwargs=kwg,
        num_pp_samples=250,
        legend=True,
    )
    # for some reason the arviz function does not create a legend with the bokeh backend despite
    # the feature being set as true. Therefore need to create a legend manually. 
    # find the line types -  all lines apart from last 2 are the MCMC samples so start from end and work backwards and the last 3 line types
    # are the 3 being used. Create labels and then add to plot
    total = len(plot[0,0].renderers)-1
    li1 = LegendItem(label=(group + ' Predictive Samples'), renderers=[plot[0,0].renderers[total-2]])
    li2 = LegendItem(label='Likelihood/Observed', renderers=[plot[0,0].renderers[total-1]])
    li3 = LegendItem(label=(group + ' Predictive Samples Mean'), renderers=[plot[0,0].renderers[total]])
    legend = Legend(items=[li1, li2, li3])
    legend.location = (10,-10)
    end_plot = plot[0][len(plot[0])-1]
    end_plot.add_layout(legend, place='right')
    end_plot.width = 800
    for p in plot[0]:
        # setting the title of the plots so have the config name at the start
        p.title.text = key+' '+p.title.text 
    return plot
# ************************************************************************************









@without_document_lock
@plot_cache
def prior_predictive_density_plot(variable, data, plot='prior_predictive'):
    """
    created the prior predictive plot, outsources the plotting to call to plot_call_ppc so that
    individual plots can be cached. Also allows for the same plotting method to be used for 
    posterior and prior ppc.
    """
    plots = pn.Column(scroll=True, max_height=750, sizing_mode='stretch_both')
    kwg = dict(height=350, width=500)
    x, y = None, None
    for key, value in data.items():
        plot = plot_call_ppc(group='Prior', key=key, var=variable, value=value)
        # **** detects the first plots axis and then locks all the other plots to the same axis
        if x == None:
            x = plot[0,0].x_range
            y = plot[0,0].y_range
        for p in plot[0]:
            p.x_range =  x
            p.y_range = y
        plots.append(row(plot[0].tolist()))
    return plots






@without_document_lock
@plot_cache
def posterior_predictive_density_plot(variable, data, percent, plot='posterior_predictive',):
    """
    similar function to the prior ppc but also handles changes in perecentages to be displayed
    """
    plots = pn.Column(scroll=True, max_height=750, sizing_mode='stretch_both')
    x, y = None,None
    kwg = dict(height=350, width=500)
    for key, value in data.items():
        plot = plot_call_ppc(group='Posterior', key=key, var=variable, value=value, percent=percent)
        # locking axis to the first plot so that all values are easily comparable
        if x == None:
            x = plot[0,0].x_range
            y = plot[0,0].y_range
        for p in plot[0]:
            p.x_range =  x
            p.y_range = y
        plots.append(row(plot[0].tolist()))
    return plots




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
        p.title.text = key+' '+p.title.text 
        if p.legend:
            p.legend.visible = False
    return plot
# ************************************************************************************


@without_document_lock
@plot_cache
def sample_trace_plot(variable, data, plot='sample_trace'):
    """
    plots the MCMC trace plot. Outsources plot call to another method to allow for
    individual plot cacheing. Just creates plots and then groups together
    """
    plots = pn.Column(scroll=True, max_height=750, sizing_mode='stretch_both')
    kwg = dict(height=200)
    x_axis_range, y_axis_range = [],[]
    for key, value in data.items():
        plot = plot_call_trace(group='', key=key, var=variable, value=value)
        plots.append(row(plot[0].tolist()))
    return plots

def compare_plot(data):
    """
    functions for creating the WAIC compare plot function. Creates data for WAIC here using the 
    dictionary of models provided. Plot doesn't need to be dynamically redrawn with interactive 
    functions so latency is not really an issue. Which is why its easier just to create the WAIC
    data here. Plot only redrawn each time a new model is added.
    """
    model_data = {}
    for key, value in data.items():
        model_data[key] = value.model_arviz_data
    comp = az.compare(
            model_data, 
            ic='waic',
            scale='log',
            )
    comp.replace([np.inf, -np.inf], np.nan)
    if comp.isnull().values.any():
        # if null values present then - in the cases ive seen - it means the model is using data
        # with missing values. Therefore notify the user that this feature is not available.
        return pn.widgets.StaticText(name='', value='Data contains missing values so can\'t compute WAIC')
    
    elif comp.shape[0] < 2:
        # for some reason this plot creates an error tha will stop the whole app from loading 
        # if only one model is plotted. Therefore notify the user that a second configuration 
        # is required before this feature is enabled.
        return pn.widgets.StaticText(name='', value='Add another configuration to compare models')

    else:
        kwg = dict(height=450, width=650,toolbar_location='right')
        plot = az.plot_compare(
                comp,
                backend='bokeh',
                show=False,
                backend_kwargs=kwg,
                order_by_rank=True,
                )
        # plot does not generate a legend automatically so create one manually here by capturing the
        # plot features and giving them labels
        li1 = LegendItem(label='WAIC', renderers=[plot.renderers[2]])
        li2 = LegendItem(label='Stadard Error', renderers=[plot.renderers[3]])
        li3 = LegendItem(label='In-Sample Deviance', renderers=[plot.renderers[4]])
        legend = Legend(items=[li1, li2, li3])
        legend.location = (10,-10)
        plot.add_layout(legend, place='right')
        plot.width = 800
        return plot



    