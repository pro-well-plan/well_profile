from .equations import *
from numpy import interp, linspace
import pandas as pd
from math import degrees
from .well import Well


def load(data, units='metric', set_start=None, equidistant=False, cells_no=None, change_azimuth=None,
         dls_resolution=30):
    """
    Load an existing wellpath.

    Arguments:
        data: excel file, dataframe or list of dictionaries containing md, tvd, inclination and azimuth
        units: 'metric' or 'english'
        set_start: set initial point in m {'north': 0, 'east': 0}
        equidistant: True to get same md difference between points
        cells_no: set number of cells if equidistant is True
        change_azimuth: add specific degrees to azimuth values along the entire well
        dls_resolution: base length to calculate dls

    Returns:
        a wellpath object with 3D position
    """

    initial_point = {'north': 0, 'east': 0}

    base_data = False
    data_initial = None

    if set_start is not None:
        for x in set_start:  # changing default values
            if x in initial_point:
                initial_point[x] = set_start[x]

    if isinstance(data, pd.DataFrame):
        base_data = True
        data_initial = data.copy()
        data.dropna(inplace=True)
        data = solve_key_similarities(data)
        data = data.to_dict('records')

    if ".xlsx" in data:
        base_data = True
        data = pd.read_excel(data)  # open excel file with pandas
        data_initial = data.copy()
        data.dropna(inplace=True)
        data = solve_key_similarities(data)
        data = data.to_dict('records')

    if ".csv" in data:
        base_data = True
        data = pd.read_csv(data)  # open csv file with pandas
        data_initial = data.copy()
        data.dropna(inplace=True)
        data = solve_key_similarities(data)
        data = data.to_dict('records')

    if type(data[0]) is dict:
        md = [x['md'] for x in data]
        inc = [x['inclination'] for x in data]
        az = [x['azimuth'] for x in data]
    else:       # if data is not a list of dicts, but a list of lists
        md, inc, az = data[:3]

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
        depth_step = md_new[1] - md_new[0]
    else:
        md_new = md
        inc_new = inc
        az_new = az
        cells_no = len(md_new)
        depth_step = None

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

    if type(data[0]) is dict and 'tvd' in data[0]:
        tvd = [x['tvd'] for x in data]
        for x, y in enumerate(tvd):     # change values to numbers if are strings
            if type(y) == str:
                tvd[x] = float(y.split(",", 1)[0])
        tvd_new = []
        for i in md_new:
            tvd_new.append(interp(i, md, tvd))
        tvd = tvd_new

    else:
        if len(data) == 4:
            tvd = data[3]
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

    data = {'md': md_new, 'tvd': tvd, 'inclination': inc_new, 'azimuth': az_new, 'dogleg': dogleg,
            'north': [n + initial_point['north'] for n in north],
            'east': [e + initial_point['east'] for e in east],
            'dlsResolution': dls_resolution,
            'depthStep': depth_step, 'cellsNo': cells_no, 'sections': sections, 'units': units}

    well = Well(data)

    if base_data:
        well._base_data = data_initial

    return well


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
