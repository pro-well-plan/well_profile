from .equations import *
from numpy import interp, linspace
import pandas as pd
from math import degrees
from .well import Well, define_sections


def load(data, set_start=None, equidistant=True, points=None, change_azimuth=None, set_info=None, calc_loc=False):
    """
    Load an existing wellpath.

    Arguments:
        data: excel file, dataframe or list of dictionaries containing md, tvd, inclination and azimuth
        set_start: set initial point in m {'north': 0, 'east': 0}
        equidistant: True to get same md difference between points
        points: set number of points if equidistant is True
        change_azimuth: add specific degrees to azimuth values along the entire well
        set_info: dict, {'dlsResolution', 'wellType': 'onshore'|'offshore', 'units': 'metric'|'english'}
        calc_loc: calculate north, east and tvd, even if this data is available

    Returns:
        a wellpath object with 3D position
    """

    info = {'dlsResolution': 30, 'wellType': 'offshore', 'units': 'metric'}

    initial_point = {'north': 0, 'east': 0}

    base_data = False
    data_initial = None

    processed = False

    if set_info is not None:
        for param in set_info:  # changing default values
            if param in info:
                info[param] = set_info[param]

    if set_start is not None:
        for x in set_start:  # changing default values
            if x in initial_point:
                initial_point[x] = set_start[x]

    if isinstance(data, pd.DataFrame):
        base_data = True
        data_initial = data.copy()
        data.dropna(axis=1, how='all', inplace=True)
        data.dropna(inplace=True)
        data = solve_key_similarities(data)
        data = data.to_dict('records')
        processed = True

    if ".xlsx" in data:
        base_data = True
        data = pd.read_excel(data)  # open excel file with pandas
        data_initial = data.copy()
        data.dropna(axis=1, how='all', inplace=True)
        data.dropna(inplace=True)
        data = solve_key_similarities(data)
        data = data.to_dict('records')
        processed = True

    if ".csv" in data:
        base_data = True
        data = pd.read_csv(data)  # open csv file with pandas
        data_initial = data.copy()
        data.dropna(axis=1, how='all', inplace=True)
        data.dropna(inplace=True)
        data = solve_key_similarities(data)
        data = data.to_dict('records')
        processed = True

    if type(data[0]) is dict:
        if not processed:
            data = solve_key_similarities(data)
        md = [x['md'] for x in data]
        inc = [x['inc'] for x in data]
        az = [x['azi'] for x in data]
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
        if points is None:
            points = len(data)
        md_new = list(linspace(min(md), max(md), num=points))
        inc_new = []
        az_new = []
        _initial_azi = 0
        _kickoff = 0
        _eob = 0
        for idx, point in enumerate(md):
            if inc[idx] != 0:
                _initial_azi = az[idx]
                _kickoff = md[idx - 1]
                _eob = point
                break
        for i in md_new:
            inc_new.append(interp(i, md, inc))
            if _kickoff <= i <= _eob:
                az_new.append(_initial_azi)
            else:
                az_new.append(interp(i, md, az))
        depth_step = md_new[1] - md_new[0]
    else:
        md_new = md
        inc_new = inc
        az_new = az
        points = len(md_new)
        depth_step = None

    dogleg = [0]
    for x in range(1, len(md_new)):
        dogleg.append(calc_dogleg(inc_new[x-1], inc_new[x], az_new[x-1], az_new[x]))

    if 'north' and 'east' in data[0] and not calc_loc:
        north = [x['north'] for x in data]
        east = [x['east'] for x in data]

        for x, y in enumerate(north):       # change values to numbers if are strings
            if type(y) == str:
                north[x] = float(y.split(",", 1)[0])
                east[x] = float(east[x].split(",", 1)[0])

        north_new = [data[0]['north']]
        east_new = [data[0]['east']]
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

    if type(data[0]) is dict and 'tvd' in data[0] and not calc_loc:
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

    data = {'md': md_new, 'tvd': tvd, 'inclination': inc_new, 'azimuth': az_new, 'dogleg': dogleg,
            'north': [n + initial_point['north'] for n in north],
            'east': [e + initial_point['east'] for e in east],
            'info': info, 'depthStep': depth_step, 'points': points, 'sections': sections}

    well = Well(data)

    if base_data:
        well._base_data = data_initial

    return well


def solve_key_similarities(data):
    md_similarities = ['MD', 'md(ft)', 'md(m)', 'MD(m)', 'MD(ft)',
                       'measureddepth', 'MeasuredDepth',
                       'measureddepth(m)', 'MeasuredDepth(m)',
                       'measureddepth(ft)', 'MeasuredDepth(ft)']

    inc_similarities = ['Inclination', 'inclination', 'Inc', 'Incl', 'incl',
                        'inclination(°)', 'Inclination(°)', 'Incl(°)',
                        'incl(°)', 'Inc(°)', 'inc(°)', 'INC', 'INC(°)', 'INCL',
                        'INCL(°)', 'Inc(deg)', 'inc(deg)']

    azi_similarities = ['az', 'az(°)',
                        'Az', 'Az(°)',
                        'AZ', 'AZ(°)',
                        'Azi', 'Azi(°)',
                        'azi(°)',
                        'AZI', 'AZI(°)',
                        'Azimuth', 'Azimuth(°)',
                        'azimuth', 'azimuth(°)',
                        'Azi(deg)', 'azi(deg)']

    tvd_similarities = ['TVD', 'TVD (m)', 'TVD (ft)', 'TVD(m)', 'TVD(ft)',
                        'tvd (m)', 'tvd (ft)', 'tvd(m)', 'tvd(ft)']

    north_similarities = ['NORTH', 'NORTH(m)', 'NORTH(ft)',
                          'North', 'North(m)', 'North(ft)',
                          'Northing(m)', 'Northing(ft)'
                          'N/S(m)', 'N/S(ft)',
                          'Ns(m)', 'Ns(ft)']

    east_similarities = ['EAST', 'EAST(m)', 'EAST(ft)',
                         'East', 'East(m)', 'East(ft)',
                         'Easting(m)', 'Easting(ft)'
                         'E/W(m)', 'E/W(ft)',
                         'Ew(m)', 'Ew(ft)']

    possible_keys = [md_similarities,
                     tvd_similarities,
                     inc_similarities,
                     azi_similarities,
                     north_similarities,
                     east_similarities]

    correct_keys = ['md', 'tvd', 'inc', 'azi', 'north', 'east']

    true_key = 0
    for i in possible_keys:
        for x in i:
            if isinstance(data, pd.DataFrame):
                data.columns = data.columns.str.replace(' ', '')
                if x in data.columns:
                    data.rename(columns={x: correct_keys[true_key]}, inplace=True)
            else:
                if x.replace(' ', '') in data[0]:
                    for point in data:
                        point[correct_keys[true_key]] = point[x]
        true_key += 1

    return data
