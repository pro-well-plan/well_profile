from .equations import *
from .plot import plot_wellpath
import pandas as pd


class Well(object):
    def __init__(self, data):
        self.depth_step = data['depthStep']
        self.cells_no = data['cellsNo']
        self.dls = calc_dls(data['dogleg'], data['md'], resolution=data['dlsResolution'])
        self.dls_resolution = data['dlsResolution']
        self.units = data['units']
        self.trajectory = []
        for point in range(len(data['md'])):
            self.trajectory.append({'md': data['md'][point],
                                    'tvd': data['tvd'][point],
                                    'inc': data['inclination'][point],
                                    'azi': data['azimuth'][point],
                                    'dl': data['dogleg'][point],
                                    'north': data['north'][point],
                                    'east': data['east'][point],
                                    'dls': self.dls[point],
                                    'sectionType': data['sections'][point]})

    def plot(self, add_well=None, names=None, dark_mode=False):
        fig = plot_wellpath(self, add_well, names, dark_mode)
        return fig

    def df(self):
        dataframe = pd.DataFrame(self.trajectory)
        return dataframe

    def add_location(self, lat, lon):
        """
        set specific location lat and lon in decimal degrees
        """
        self.location = {'lat': lat, 'lon': lon}
