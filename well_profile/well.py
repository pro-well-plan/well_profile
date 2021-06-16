from .equations import *
from .plot import plot_wellpath, plot_top_view, plot_vs
import pandas as pd


class Well(object):
    def __init__(self, data):
        self.depth_step = data['depthStep']
        self.points = data['points']
        self.info = data['info']
        data['dls'] = calc_dls(data['dogleg'], data['md'], resolution=self.info['dlsResolution'])
        data['delta'] = get_delta(data)
        self.trajectory = []
        for point in range(len(data['md'])):
            self.trajectory.append({'md': data['md'][point],
                                    'tvd': round(data['tvd'][point], 2),
                                    'inc': data['inclination'][point],
                                    'azi': data['azimuth'][point],
                                    'dl': data['dogleg'][point],
                                    'north': round(data['north'][point], 2),
                                    'east': round(data['east'][point], 2),
                                    'dls': data['dls'][point],
                                    'sectionType': data['sections'][point],
                                    'delta': data['delta'][point]})

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
            raise ValueError('The plot type "{}" is not recognised'.format(default['plot_type'] ))

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


def define_sections(tvd, inc):
    sections = ['vertical', 'vertical']
    for z in range(2, len(tvd)):
        delta_tvd = round(tvd[z] - tvd[z - 1], 9)
        if inc[z] == 0:  # Vertical Section
            sections.append('vertical')
        else:
            if round(inc[z], 2) == round(inc[z - 1], 2):
                if delta_tvd == 0:
                    sections.append('horizontal')  # Horizontal Section
                else:
                    sections.append('hold')  # Straight Inclined Section
            else:
                if inc[z] > inc[z - 1]:  # Built-up Section
                    sections.append('build-up')
                if inc[z] < inc[z - 1]:  # Drop-off Section
                    sections.append('drop-off')

    return sections


def get_delta(trajectory):
    delta = [{'md': 0,
              'tvd': 0,
              'inc': 0,
              'azi': 0,
              'dl': 0,
              'dls': 0,
              'north': 0,
              'east': 0}]

    for idx in range(1, len(trajectory['md'])):
        delta.append({'md': trajectory['md'][idx] - trajectory['md'][idx-1],
                      'tvd': trajectory['tvd'][idx] - trajectory['tvd'][idx-1],
                      'inc': trajectory['inclination'][idx] - trajectory['inclination'][idx-1],
                      'azi': trajectory['azimuth'][idx] - trajectory['azimuth'][idx-1],
                      'dl': trajectory['dogleg'][idx] - trajectory['dogleg'][idx-1],
                      'dls': trajectory['dls'][idx] - trajectory['dls'][idx-1],
                      'north': trajectory['north'][idx] - trajectory['north'][idx-1],
                      'east': trajectory['east'][idx] - trajectory['east'][idx-1]})

    return delta
