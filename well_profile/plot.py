import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_wellpath(well, **kwargs):
    """
    Plot a 3D Wellpath.

    Keyword Arguments:
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

    data = {'add_well': None, 'names': None, 'style': None}
    for key, value in kwargs.items():
        data[key] = value

    units = well.info['units']

    well1 = pd.DataFrame(well.trajectory)
    well1["well"] = 1
    result = well1

    if data['add_well'] is not None:
        wells = []

        if type(data['add_well']) is not list:
            data['add_well'] = [data['add_well']]

        well_no = 2
        for x in data['add_well']:
            new_well = pd.DataFrame(x.trajectory)
            new_well["well"] = well_no
            wells.append(new_well)
            well_no += 1

        all_wells = well1.append(wells)
        result = all_wells

    if data['names'] is not None:

        if type(data['names']) is not list:
            data['names'] = [data['names']]

        well_no = 1
        for x in data['names']:
            result.replace({'well': {well_no: x}}, inplace=True)
            well_no += 1

    style = define_style(data['style'])

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
    include_logo(fig, style['darkMode'], plot_type='3D', color=style['color'])
    fig.update_layout(title='Wellbore Trajectory - 3D View')

    return fig


def plot_top_view(well, **kwargs):
    data = {'add_well': None, 'names': None, 'style': None}
    for key, value in kwargs.items():
        data[key] = value

    wells = [well]
    units = well.info['units']

    if data['add_well'] is not None:
        if type(data['add_well']) is not list:
            data['add_well'] = [data['add_well']]
        wells += data['add_well']

    if data['names']:
        if type(data['names']) is not list:
            data['names'] = [data['names']]
    else:
        data['names'] = []
        for idx in range(len(wells)):
            data['names'].append('well ' + str(idx + 1))

    fig = go.Figure()

    for idx, w in enumerate(wells):
        fig.add_trace(go.Scatter(
            x=[point['east'] for point in w.trajectory],
            y=[point['north'] for point in w.trajectory],
            hovertemplate='<b>North</b>: %{y:.2f}<br>' + '<b>East</b>: %{x}<br>',
            showlegend=False, name=data['names'][idx]))

    if units == 'metric':
        fig.update_layout(xaxis_title='East, m',
                          yaxis_title='North, m')
    else:
        fig.update_layout(xaxis_title='East, ft',
                          yaxis_title='North, ft')

    fig.update_layout(title='Wellbore Trajectory - Top View', hovermode='closest')

    style = define_style(data['style'])
    include_logo(fig, style['darkMode'], plot_type='top')
    fig.layout.template = style['darkMode']

    return fig


def plot_vs(well, **kwargs):
    unit_system = well.info['units']
    dls_res = well.info['dlsResolution']
    data = {'y_axis': 'md', 'x_axis': 'inc', 'add_well': None, 'names': None, 'style': None}
    for key, value in kwargs.items():
        data[key] = value

    possible_props = ['md', 'tvd', 'north', 'east', 'inc', 'azi', 'dl', 'dls']
    for prop in [data['x_axis'], data['y_axis']]:
        if prop not in possible_props:
            raise ValueError('The axis "{}" is not recognised'.format(prop))

    wells = [well]

    if data['add_well'] is not None:
        if type(data['add_well']) is not list:
            data['add_well'] = [data['add_well']]
        wells += data['add_well']

    if data['names']:
        if type(data['names']) is not list:
            data['names'] = [data['names']]
    else:
        data['names'] = []
        for idx in range(len(wells)):
            data['names'].append('well ' + str(idx+1))

    fig = go.Figure()

    for idx, w in enumerate(wells):
        fig.add_trace(go.Scatter(
            x=[point[data['x_axis']] for point in w.trajectory],
            y=[point[data['y_axis']] for point in w.trajectory],
            hovertemplate='<b>y</b>: %{y:.2f}<br>' + '<b>x</b>: %{x:.2f}<br>',
            showlegend=False, name=data['names'][idx]))

    units = ['m', '°']
    for key, axis, in {'0': data['x_axis'], '1': data['y_axis']}.items():
        if axis in ['md', 'tvd', 'north', 'east']:
            if unit_system == 'metric':
                units[int(key)] = 'm'
            else:
                units[int(key)] = 'ft'
        elif axis in ['inc', 'azi', 'dl']:
            units[int(key)] = '°'
        elif axis == 'dls':
            if unit_system == 'metric':
                units[int(key)] = '°/' + str(dls_res) + 'm'
            else:
                units[int(key)] = '°/' + str(dls_res) + 'ft'

    style = define_style(data['style'])
    include_logo(fig, style['darkMode'], plot_type='vs')
    fig.layout.template = style['darkMode']

    fig.update_layout(xaxis_title=data['x_axis'] + ', ' + units[0],
                      yaxis_title=data['y_axis'] + ', ' + units[1],
                      title='Wellbore Trajectory - ' + data['x_axis'] + ' vs ' + data['y_axis'],
                      hovermode='closest')

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


def include_logo(fig, dark=None, plot_type='3D', color=None):
    if not color:
        if not dark:
            y = 0.91
        else:
            y = 0.95
    else:
        if not dark:
            y = 0.97
        else:
            y = 1
    if dark == 'plotly_dark':
        if plot_type != '3D':
            y = 1.03
        fig.update_layout(images=[dict(
                          source="https://raw.githubusercontent.com/jcamiloangarita/opensource_apps/master/"
                                 "resources/pwp-logo-dark.png",
                          xref="paper", yref="paper",
                          x=0.5, y=y,
                          sizex=0.12, sizey=0.12,
                          xanchor="right", yanchor="bottom")])
    else:
        if plot_type != '3D':
            y = 0.99
        fig.update_layout(images=[dict(
                          source="https://avatars.githubusercontent.com/u/53001276?v=4",
                          xref="paper", yref="paper",
                          x=0.35, y=y,
                          sizex=0.2, sizey=0.2,
                          xanchor="right", yanchor="bottom")])
