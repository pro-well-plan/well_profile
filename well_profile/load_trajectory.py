from .plot import plot_wellpath
from numpy import interp, arange
from math import radians, sin, cos, degrees, acos, tan
import pandas as pd


def load(data, grid_length=50, units='metric'):
    """
    Load an existing wellpath.
    :param data: excel file, dataframe or list of dictionaries containing md, tvd, inclination and azimuth
    :param grid_length: cell's length, m or ft
    :param units: 'metric' or 'english'
    :return: a wellpath object with 3D position
    """

    if isinstance(data, pd.DataFrame):
        data_initial = data.copy()
        data.dropna(inplace=True)
        data = data.to_dict('records')

    if ".xlsx" in data:
        data = pd.read_excel(data)  # open excel file with pandas
        data_initial = data.copy()
        data.dropna(inplace=True)
        data = data.to_dict('records')

    if ".csv" in data:
        data = pd.read_csv(data)  # open csv file with pandas
        data_initial = data.copy()
        data.dropna(inplace=True)
        data = data.to_dict('records')

    md = [x['md'] for x in data]
    tvd = [x['tvd'] for x in data]
    inc = [x['inclination'] for x in data]
    az = [x['azimuth'] for x in data]
    deltaz = grid_length

    md_new = list(arange(0, max(md) + deltaz, deltaz))
    tvd_new = [0]
    inc_new = [0]
    az_new = [0]
    for i in md_new[1:]:
        tvd_new.append(interp(i, md, tvd))
        inc_new.append(interp(i, md, inc))
        az_new.append(interp(i, md, az))
    zstep = len(md_new)

    dogleg = [0]
    for x in range(1, len(md_new)):
        dogleg.append(acos(
            cos(radians(inc_new[x])) * cos(radians(inc_new[x - 1]))
            - sin(radians(inc_new[x])) * sin(radians(inc_new[x - 1])) * (1 - cos(radians(az_new[x] - az_new[x - 1])))
        ))

    if 'north' and 'east' in data[0]:
        north = [x['north'] for x in data]
        east = [x['east'] for x in data]
        north_new = [0]
        east_new = [0]
        for i in md_new[1:]:
            north_new.append(interp(i, md, north))
            east_new.append(interp(i, md, east))
        north = north_new
        east = east_new

    else:
        north = [0]
        east = [0]
        for x in range(1, len(md_new)):
            delta_md = md_new[x] - md_new[x - 1]
            if dogleg[x] == 0:
                RF = 1
            else:
                RF = tan(dogleg[x] / 2) / (dogleg[x] / 2)
            north_delta = 0.5 * delta_md * (sin(radians(inc_new[x - 1])) * cos(radians(az_new[x - 1]))
                                            + sin(radians(inc_new[x])) * cos(radians(az_new[x]))) * RF
            north.append(north[-1] + north_delta)
            east_delta = 0.5 * delta_md * (sin(radians(inc_new[x - 1])) * sin(radians(az_new[x - 1]))
                                           + sin(radians(inc_new[x])) * sin(radians(az_new[x]))) * RF
            east.append(east[-1] + east_delta)

    dogleg = [degrees(x) for x in dogleg]

    # Defining type of section
    sections = ['vertical', 'vertical']
    for z in range(2, len(tvd_new)):
        delta_tvd = round(tvd_new[z] - tvd_new[z - 1], 9)
        if inc_new[z] == 0:  # Vertical Section
            sections.append('vertical')
        else:
            if round(inc_new[z], 2) == round(inc_new[z - 1], 2):
                if delta_tvd == 0:
                    sections.append('horizontal')  # Horizontal Section
                else:
                    sections.append('hold')  # Straight Inclined Section
            else:
                if inc_new[z] > inc_new[z - 1]:  # Built-up Section
                    sections.append('build-up')
                if inc_new[z] < inc_new[z - 1]:  # Drop-off Section
                    sections.append('drop-off')

    class WellDepths(object):
        def __init__(self):
            self.md = md_new
            self.tvd = tvd_new
            self.inclination = inc_new
            self.azimuth = az_new
            self.dogleg = dogleg
            self.deltaz = deltaz
            self.zstep = zstep
            self.north = north
            self.east = east
            self.sections = sections
            self.units = units

        def plot(self, add_well=None, names=None):
            fig = plot_wellpath(self, add_well, names)
            return fig

        def df(self):
            data_dict = {'md': self.md, 'tvd': self.tvd, 'inclination': self.inclination,
                         'azimuth': self.azimuth, 'north': self.north, 'east': self.east}
            dataframe = pd.DataFrame(data_dict)
            return dataframe

        def initial(self):
            return data_initial

    return WellDepths()
