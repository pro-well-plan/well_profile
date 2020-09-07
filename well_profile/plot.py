import pandas as pd
import plotly.express as px


def plot_wellpath(wellpath, add_well=None, names=None):
    """
    Plot a 3D Wellpath.
    :param wellpath: a wellpath object with 3D position,
    :param add_well: include a new well or list of wells
    :param names: set name or list of names for wells included in the plot
    :return: 3D Plot - plotly.graph_objects.Figure
    """

    units = wellpath.units

    well1 = pd.DataFrame(list(zip(wellpath.tvd, wellpath.north, wellpath.east)), columns=['tvd', 'north', 'east'])
    well1["well"] = 1
    result = well1

    if add_well is not None:
        wells = []

        if type(add_well) is not list:
            add_well = [add_well]

        well_no = 2
        for x in add_well:
            new_well = pd.DataFrame(list(zip(x.tvd, x.north, x.east)), columns=['tvd', 'north', 'east'])
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

    fig = px.line_3d(result, x="east", y="north", z="tvd", color='well')

    if units == 'metric':
        fig.update_layout(scene=dict(
            xaxis_title='East, m',
            yaxis_title='North, m',
            zaxis_title='TVD, m'))
    else:
        fig.update_layout(scene=dict(
            xaxis_title='East, ft',
            yaxis_title='North, ft',
            zaxis_title='TVD, ft'))
    fig.update_scenes(zaxis_autorange="reversed")

    return fig
