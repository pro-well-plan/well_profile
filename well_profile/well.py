from .equations import *
from .plot import plot_wellpath, plot_top_view, plot_vs
import pandas as pd


class Well(object):
    def __init__(self, data):
        self.info = data['info']
        self.trajectory = data['trajectory']
        for idx, point in enumerate(self.trajectory):
            if idx > 0:
                delta_md = point['md'] - self.trajectory[idx - 1]['md']
                point['dls'] = calc_dls(point, delta_md, resolution=self.info['dlsResolution'])
                point['delta'] = get_delta(point, self.trajectory[idx-1])
            else:
                point['dls'] = 0
                point['delta'] = get_delta(point)
        self.npoints = len(self.trajectory)

    def plot(self, **kwargs):
        default = {'plot_type': '3d', 'add_well': None, 'names': None, 'style': None, 'y_axis': 'md', 'x_axis': 'inc'}
        for key, value in kwargs.items():
            default[key] = value

        if default['plot_type'] == '3d':
            fig = plot_wellpath(self, add_well=default['add_well'], names=default['names'], style=default['style'])
            return fig
        elif default['plot_type'] == 'top':
            fig = plot_top_view(self, add_well=default['add_well'], names=default['names'], style=default['style'])
            return fig
        elif default['plot_type'] == 'vs':
            fig = plot_vs(self, y_axis=default['y_axis'], x_axis=default['x_axis'], add_well=default['add_well'],
                          names=default['names'], style=default['style'])
            return fig
        else:
            raise ValueError('The plot type "{}" is not recognised'.format(default['plot_type']))

    def df(self):
        dataframe = pd.DataFrame(self.trajectory)
        return dataframe

    def add_location(self, lat, lon):
        """
        set specific location lat and lon in decimal degrees
        """
        self.info['location'] = {'lat': lat, 'lon': lon}

    def add_reference(self, references):
        self.info['rkb'] = references['rkb']
        if 'waterDepth' in references:
            self.info.update({'waterDepth': references['waterDepth'],
                              'seabed': references['rkb'] + references['waterDepth']})

    def get_point(self, md):
        return interp_pt(md, self.trajectory)


def define_section(p2, p1=None):

    if not p1:
        return 'vertical'

    else:
        if p2['inc'] == p1['inc'] == 0:
            return 'vertical'
        else:
            if round(p2['inc'], 2) == round(p1['inc'], 2):
                if p2['tvd'] == p1['tvd'] == 0:
                    return 'horizontal'  # Horizontal Section
                else:
                    return 'hold'  # Straight Inclined Section
            else:
                if p2['inc'] > p1['inc']:
                    return 'build-up'   # Built-up Section
                if p2['inc'] < p1['inc']:
                    return 'drop-off'   # Drop-off Section


def get_delta(p2, p1=None):

    if not p1:
        return {'md': 0, 'tvd': 0, 'inc': 0, 'azi': 0, 'dl': 0, 'dls': 0, 'north': 0, 'east': 0}

    else:
        delta_dict = {}
        for param in ['md', 'tvd', 'inc', 'azi', 'dl', 'dls', 'north', 'east']:
            delta_dict.update({param: p2[param] - p1[param]})

    return delta_dict
