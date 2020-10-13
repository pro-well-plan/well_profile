from .plot import plot_wellpath
from .equations import *
from numpy import interp, linspace
import pandas as pd
from math import degrees


def load(data, units='metric', set_start=None, equidistant=False, cells_no=None, change_azimuth=None):
    """
    Load an existing wellpath.
    :param data: excel file, dataframe or list of dictionaries containing md, tvd, inclination and azimuth
    :param units: 'metric' or 'english'
    :param set_start: set initial point in m {'north': 0, 'east': 0}
    :param equidistant: True to get same md difference between points
    :param cells_no: set number of cells if equidistant is True
    :param change_azimuth: add specific degrees to azimuth values along the entire well
    :return: a wellpath object with 3D position
    """

    initial_point = {'north': 0, 'east': 0}

    if set_start is not None:
        for x in set_start:  # changing default values
            if x in initial_point:
                initial_point[x] = set_start[x]

    if isinstance(data, pd.DataFrame):
        data_initial = data.copy()
        data.dropna(inplace=True)
        data = solve_key_similarities(data)
        data = data.to_dict('records')

    if ".xlsx" in data:
        data = pd.read_excel(data)  # open excel file with pandas
        data_initial = data.copy()
        data.dropna(inplace=True)
        data = solve_key_similarities(data)
        data = data.to_dict('records')

    if ".csv" in data:
        data = pd.read_csv(data)  # open csv file with pandas
        data_initial = data.copy()
        data.dropna(inplace=True)
        data = solve_key_similarities(data)
        data = data.to_dict('records')

    md = [x['md'] for x in data]
    inc = [x['inclination'] for x in data]
    az = [x['azimuth'] for x in data]
    if change_azimuth is not None:
        for a in range(len(az)):
            az[a] += change_azimuth

    for x, y in enumerate(md):      # change values to numbers if are strings
        if type(y) == str:
            md[x] = float(y.split(",", 1)[0])
            inc[x] = float(inc[x].split(",", 1)[0])
            az[x] = float(az[x].split(",", 1)[0])

    if equidistant:
        if cells_no is None:
            cells_no = len(data)
        md_new = list(linspace(min(md), max(md), num=cells_no))
        inc_new = []
        az_new = []
        for i in md_new:
            inc_new.append(interp(i, md, inc))
            az_new.append(interp(i, md, az))
    else:
        md_new = md
        inc_new = inc
        az_new = az
        cells_no = len(md_new)

    depth_step = md_new[1] - md_new[0]

    dogleg = [0]
    for x in range(1, len(md_new)):
        dogleg.append(calc_dogleg(inc_new[x-1], inc_new[x], az_new[x-1], az_new[x]))

    if 'north' and 'east' in data[0]:
        north = [x['north'] for x in data]
        east = [x['east'] for x in data]

        for x, y in enumerate(north):       # change values to numbers if are strings
            if type(y) == str:
                north[x] = float(y.split(",", 1)[0])
                east[x] = float(east[x].split(",", 1)[0])

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
            north.append(calc_north(north[-1],
                                    md_new[x-1], md_new[x],
                                    inc_new[x-1], inc_new[x],
                                    az_new[x-1], az_new[x],
                                    dogleg[x]))
            east.append(calc_east(east[-1],
                                  md_new[x - 1], md_new[x],
                                  inc_new[x - 1], inc_new[x],
                                  az_new[x - 1], az_new[x],
                                  dogleg[x]))

    if 'tvd' in data[0]:
        tvd = [x['tvd'] for x in data]
        for x, y in enumerate(tvd):     # change values to numbers if are strings
            if type(y) == str:
                tvd[x] = float(y.split(",", 1)[0])
        tvd_new = []
        for i in md_new:
            tvd_new.append(interp(i, md, tvd))
        tvd = tvd_new

    else:
        tvd = [md_new[0]]
        for x in range(1, len(md_new)):
            tvd.append(calc_tvd(tvd[-1],
                                md_new[x-1],
                                md_new[x],
                                inc_new[x-1],
                                inc_new[x],
                                dogleg[x]))

    dogleg = [degrees(x) for x in dogleg]

    # Defining type of section
    sections = define_sections(tvd, inc_new)

    class WellDepths(object):
        def __init__(self):
            self.md = md_new
            self.tvd = tvd
            self.inclination = inc_new
            self.azimuth = az_new
            self.dogleg = dogleg
            self.depth_step = depth_step
            self.cells_no = cells_no
            self.north = [n + initial_point['north'] for n in north]
            self.east = [e + initial_point['east'] for e in east]
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


def solve_key_similarities(data):
    md_similarities = ['MD', 'MD (ft)', 'MD (m)', 'measured depth', 'Measured Depth',
                       'md (ft)', 'md (m)', 'MD(m)', 'MD(ft)', 'measured depth (ft)', 'Measured Depth (ft)',
                       'measured depth (m)', 'Measured Depth (m)', 'measured depth(m)', 'Measured Depth(m)',
                       'measured depth(ft)', 'Measured Depth(ft)']

    inc_similarities = ['Inclination', 'inc', 'Inc', 'Incl', 'incl', 'Inc (°)', 'inc (°)',
                        'Inclination (°)', 'Incl (°)', 'incl (°)', 'Inclination(°)', 'Incl(°)',
                        'incl(°)', 'Inc(°)', 'inc(°)', 'INC', 'INC(°)', 'INC (°)', 'INCL',
                        'INCL(°)', 'INCL (°)']

    azi_similarities = ['az', 'az(°)', 'az (°)',
                        'Az', 'Az(°)', 'Az (°)',
                        'AZ', 'AZ(°)', 'AZ (°)',
                        'Azi', 'Azi(°)', 'Azi (°)',
                        'azi', 'azi(°)', 'azi (°)',
                        'AZI', 'AZI(°)', 'AZI (°)',
                        'Azimuth', 'Azimuth(°)', 'Azimuth (°)']

    tvd_similarities = ['TVD', 'TVD (m)', 'TVD (ft)',
                        'TVD(m)', 'TVD(ft)']

    north_similarities = ['NORTH', 'NORTH(m)', 'NORTH(ft)',
                          'NORTH (m)', 'NORTH (ft)',
                          'North', 'North(m)', 'North(ft)',
                          'North (m)', 'North (ft)',
                          'Northing(m)', 'Northing(ft)'
                                         'Northing (m)', ' Northing(ft)'
                                                         'N/S (m)', 'N/S (ft)',
                          'N/S(m)', 'N/S(ft)',
                          'Ns (m)', 'Ns (ft)',
                          'Ns(m)', 'Ns(ft)']

    east_similarties = ['EAST', 'EAST(m)', 'EAST(ft)',
                        'EAST (m)', 'EAST (ft)',
                        'East', 'East(m)', 'East(ft)',
                        'East (m)', 'East (ft)',
                        'Easting(m)', 'Easting(ft)'
                                      'Easting (m)', ' Easting(ft)'
                                                     'E/W (m)', 'E/W (ft)',
                        'E/W(m)', 'E/W(ft)',
                        'Ew (m)', 'Ew (ft)',
                        'Ew(m)', 'Ew(ft)']

    possible_keys = [md_similarities,
                     tvd_similarities,
                     inc_similarities,
                     azi_similarities,
                     north_similarities,
                     east_similarties]

    correct_keys = ['md', 'tvd', 'inclination', 'azimuth', 'north', 'east']

    true_key = 0
    for i in possible_keys:
        for x in i:
            if x in data.columns:
                data.rename(columns={x: correct_keys[true_key]}, inplace=True)
        true_key += 1

    return data


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
