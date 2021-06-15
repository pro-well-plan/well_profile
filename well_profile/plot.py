import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_wellpath(well, add_well=None, names=None, style=None):
    """
    Plot a 3D Wellpath.

    Arguments:
        well: a well object with 3D position,
        add_well: include a new well or list of wells
        names: set name or list of names for wells included in the plot
        style: {'darkMode': bool, # activate dark mode. default = False
                'color': str, # color by specific property. e.g. 'dls'|'dl'|'tvd'|'md'|'inc'|'azi'. default = None
                'size': num, # marker size. default = 2
                }

    Returns:
        3D Plot - plotly.graph_objects.Figure
    """

    units = well.info['units']

    well1 = pd.DataFrame(well.trajectory)
    well1["well"] = 1
    result = well1

    if add_well is not None:
        wells = []

        if type(add_well) is not list:
            add_well = [add_well]

        well_no = 2
        for x in add_well:
            new_well = pd.DataFrame(x.trajectory)
            new_well["well"] = well_no
            wells.append(new_well)
            well_no += 1

        all_wells = well1.append(wells)
        result = all_wells

    if names is not None:

        if type(names) is not list:
            names = [names]

        well_no = 1
        for x in names:
            result.replace({'well': {well_no: x}}, inplace=True)
            well_no += 1

    style = define_style(style)

    if style['color'] is None:
        color = 'well'
        fig = px.line_3d(result, x="east", y="north", z="tvd", color=color)

    else:
        fig = go.Figure(
            data=[go.Scatter3d(x=result['east'],
                               y=result['north'],
                               z=result['tvd'],
                               mode='markers',
                               marker=dict(
                                    size=style['size'],
                                    color=result[style['color']],  # set color to an array/list of desired values
                                    showscale=True,
                                    opacity=0.8),
                               legendgroup=True,
                               hovertemplate='%{text}<extra></extra><br>' + '<b>North</b>: %{y:.2f}<br>' +
                                             '<b>East</b>: %{x}<br>' + '<b>TVD</b>: %{z}<br>',
                               text=result['well'])])

    if units == 'metric':
        fig.update_layout(scene=dict(
            xaxis_title='East, m',
            yaxis_title='North, m',
            zaxis_title='TVD, m',
            aspectmode='manual'))
    else:
        fig.update_layout(scene=dict(
            xaxis_title='East, ft',
            yaxis_title='North, ft',
            zaxis_title='TVD, ft',
            aspectmode='manual'))
    fig.update_scenes(zaxis_autorange="reversed")
    fig.layout.template = style['darkMode']
    fig.update_layout(title='Wellbore Trajectory - 3D View')

    return fig


def plot_top_view(well, add_well=None, names=None, style=None):
    wells = [well]

    if add_well is not None:
        if type(add_well) is not list:
            add_well = [add_well]
        wells += add_well

    if names:
        if type(names) is not list:
            names = [names]
    else:
        names = []
        well_no = 1
        for idx, well in enumerate(wells):
            names.append('well ' + str(well_no))
            well_no += 1

    fig = go.Figure()

    for idx, w in enumerate(wells):
        fig.add_trace(go.Scatter(
            x=[point['east'] for point in w.trajectory],
            y=[point['north'] for point in w.trajectory],
            hovertemplate='<b>North</b>: %{y:.2f}<br>' + '<b>East</b>: %{x}<br>',
            showlegend=False, name=names[idx]))

    if well.info['units'] == 'metric':
        fig.update_layout(xaxis_title='East, m',
                          yaxis_title='North, m')
    else:
        fig.update_layout(xaxis_title='East, ft',
                          yaxis_title='North, ft')

    fig.update_layout(title='Wellbore Trajectory - Top View')
    style = define_style(style)
    fig.layout.template = style['darkMode']

    return fig


def define_style(style):
    set_style = {'darkMode': False, 'color': None, 'size': 2}
    if style is not None:
        for key in style.keys():
            set_style[key] = style[key]

    if set_style['darkMode']:
        set_style['darkMode'] = 'plotly_dark'
    else:
        set_style['darkMode'] = None

    return set_style
