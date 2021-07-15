from .equations import *
import pandas as pd
from math import degrees
from .well import Well, define_section


def load(data, **kwargs):
    """
    Load an existing wellpath.

    Parameters
    ----------
    data:
        Excel file, dataframe or list of dictionaries.
        Must contain at least md, inclination and azimuth. Can also contain tvd, northing and easting.

    Keyword Args
    ------------
        set_start: dict, None
            set initial point in m {'north': 0, 'east': 0}.
        change_azimuth: float, int, None
            add specific degrees to azimuth values along the entire well.
        set_info: dict, None
            dict, {'dlsResolution', 'wellType': 'onshore'|'offshore', 'units': 'metric'|'english'}.
        calc_loc: bool
            calculate north, east and tvd, even if this data is available.


    Returns
    -------
    well: well object
        A wellpath object with 3D position
    """

    # Settings
    params = {'set_start': None, 'change_azimuth': None, 'set_info': None}
    for key, value in kwargs.items():
        params[key] = value
    set_start = params['set_start']
    change_azimuth = params['change_azimuth']
    set_info = params['set_info']

    info = {'dlsResolution': 30, 'wellType': 'offshore', 'units': 'metric'}

    initial_point = {'north': 0, 'east': 0}

    base_data = False
    data_initial = None
    processed = False

    # PROCESSING DATA

    if isinstance(set_info, dict):
        for param in set_info:  # changing default values
            if param in info:
                info[param] = set_info[param]

    if isinstance(set_start, dict):
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

    # DEALING WITH NAN-DATA
    for x, y in enumerate(md):      # change values to numbers if are strings
        if type(y) == str:
            md[x] = float(y.split(",", 1)[0])
            inc[x] = float(inc[x].split(",", 1)[0])
            az[x] = float(az[x].split(",", 1)[0])

    # GENERAL CHANGE IN AZIMUTH
    if change_azimuth is not None:
        for a in range(len(az)):
            az[a] += change_azimuth

    # CREATING TRAJECTORY POINTS
    trajectory = [{'md': 0, 'inc': 0, 'azi': 0, 'dl': 0, 'tvd': 0, 'sectionType': 'vertical', 'pointType': 'survey'}]
    trajectory[-1].update(initial_point)
    for idx, md in enumerate(md):
        if idx > 0:
            dogleg = calc_dogleg(inc[idx-1], inc[idx], az[idx-1], az[idx])
            point = {'md': md, 'inc': inc[idx], 'azi': az[idx],
                     'north': calc_north(trajectory[-1]['north'], trajectory[-1]['md'], md,
                                         trajectory[-1]['inc'], inc[idx],
                                         trajectory[-1]['azi'], az[idx],
                                         dogleg),
                     'east': calc_east(trajectory[-1]['east'], trajectory[-1]['md'], md,
                                       trajectory[-1]['inc'], inc[idx],
                                       trajectory[-1]['azi'], az[idx],
                                       dogleg),
                     'tvd': calc_tvd(trajectory[-1]['tvd'], trajectory[-1]['md'], md,
                                     trajectory[-1]['inc'], inc[idx], dogleg),
                     'dl': degrees(dogleg),
                     'pointType': 'survey'
                     }
            point['sectionType'] = define_section(point, trajectory[-1])
            trajectory.append(point)

    well = Well({'trajectory': trajectory, 'info': info})

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
