from math import atan, degrees, radians, asin
from numpy import linspace
import pandas as pd
from .load_trajectory import load


def two_points(points, inner_points=20):
    """
    Arguments:
        points: {'kickoff':{'north': num, 'east': num, 'tvd': num},
                 'target': {'north': num, 'east': num, 'tvd': num}}
        inner_points: number of points between curved zone

    Returns:
        a wellpath object with 3D position
    """

    if 'north' not in points['kickoff']:
        points['kickoff']['north'] = 0

    if 'east' not in points['kickoff']:
        points['kickoff']['east'] = 0

    point_1 = points['kickoff']
    point_2 = points['target']

    # set first section
    trajectory = [{'md': 0, 'inc': 0, 'azi': 0},
                  {'md': point_1['tvd'], 'inc': 0, 'azi': 0}]

    # calculate deltas
    delta = {'vertical': point_2['tvd'] - point_1['tvd'],
             'north': point_2['north'] - point_1['north'],
             'east': point_2['east'] - point_1['east']}

    delta['horizontal'] = (delta['north']**2 + delta['east']**2)**0.5

    # Define azimuth
    azimuth = 0
    if delta['north'] != 0 and delta['east'] != 0:
        beta = degrees(atan(delta['north'] / delta['east']))
        if delta['east'] > 0:
            azimuth = 90 - beta
        else:
            azimuth = 270 - beta

    else:
        if delta['north'] == 0:
            if delta['east'] > 0:
                azimuth = 90
            else:
                azimuth = 270
        if delta['east'] == 0:
            if delta['north'] > 0:
                azimuth = 0
            else:
                azimuth = 180

    # 3 cases comparing vertical and horizontal displacement
    steps = inner_points + 1
    if delta['vertical'] == delta['horizontal']:
        radius = delta['horizontal']
        theta = 90
        arc = radius * radians(theta)

        new_md = linspace(point_1['tvd']+arc/steps, point_1['tvd']+arc, steps)
        new_inc = linspace(theta/steps, theta, steps)

        for md, inc in zip(new_md, new_inc):
            trajectory.append({'md': md, 'inc': inc, 'azi': azimuth})

        well = load(pd.DataFrame(trajectory), equidistant=False, set_start=point_1)

        return well

    if delta['vertical'] < delta['horizontal']:
        # curve section
        radius = delta['vertical']
        theta = 90
        arc = radius * radians(theta)

        new_md = linspace(point_1['tvd'] + arc / steps, point_1['tvd'] + arc, steps)
        new_inc = linspace(theta / steps, theta, steps)
        for md, inc in zip(new_md, new_inc):
            trajectory.append({'md': md, 'inc': inc, 'azi': azimuth})

        # horizontal section
        trajectory.append({'md': trajectory[-1]['md']+(delta['horizontal']-delta['vertical']), 'inc': 90,
                           'azi': trajectory[-1]['azi']})

        well = load(pd.DataFrame(trajectory), equidistant=False, set_start=point_1)

        return well

    if delta['vertical'] > delta['horizontal']:
        if delta['horizontal'] != 0:
            radius = (delta['horizontal']**2 + delta['vertical']**2)/(2*delta['horizontal'])
            theta = degrees(asin(delta['vertical']/radius))
            arc = radius * radians(theta)
            new_md = linspace(point_1['tvd'] + arc / steps, point_1['tvd'] + arc, steps)
            new_inc = linspace(theta / steps, theta, steps)
        else:
            new_md = [point_2['tvd']]
            new_inc = [0]
        for md, inc in zip(new_md, new_inc):
            trajectory.append({'md': md, 'inc': inc, 'azi': azimuth})

        well = load(pd.DataFrame(trajectory), equidistant=False, set_start=point_1)

        return well
