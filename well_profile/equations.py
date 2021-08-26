from math import *
from numpy import pi


def calc_dogleg(inc1, inc2, azi1, azi2):
    """
    Calculate dogleg between two points
    :param inc1: inclination at point 1
    :param inc2: inclination at point 2
    :param azi1: azimuth at point 1
    :param azi2: azimuth at point 2
    :return: dogleg in radians
    """

    if inc1 == inc2 and azi1 == azi2:
        dl = 0
    else:
        inner_value = cos(radians(inc1)) * cos(radians(inc2)) + sin(radians(inc1)) * sin(radians(inc2)) * \
            cos(radians(azi2 - azi1))
        if inner_value > 1:
            inner_value = 1
        if inner_value < -1:
            inner_value = -1
        dl = acos(inner_value)
    return dl


def calc_north(north_prev, md1, md2, inc1, inc2, azi1, azi2, dogleg):
    """
    Calculate north coordinate of certain point using the previous one and the minimum curvature method
    :param north_prev: north coordinate at previous point (point 1)
    :param md1: measured depth at point 1
    :param md2: measured depth at point 2
    :param inc1: inclination at point 1
    :param inc2: inclination at point 2
    :param azi1: azimuth at point 1
    :param azi2: azimuth at point 2
    :param dogleg: dogleg at point 2
    :return: north coordinate at the new point (point 2)
    """
    rf = calc_rf(dogleg)
    delta_md = md2 - md1
    north_delta = 0.5 * delta_md * (sin(radians(inc1)) * cos(radians(azi1))
                                    + sin(radians(inc2)) * cos(radians(azi2))) * rf
    north_new = north_prev + north_delta

    return north_new


def calc_east(east_prev, md1, md2, inc1, inc2, azi1, azi2, dogleg):
    """
    Calculate east coordinate of certain point using the previous one and the minimum curvature method
    :param east_prev: east coordinate at previous point (point 1)
    :param md1: measured depth at point 1
    :param md2: measured depth at point 2
    :param inc1: inclination at point 1
    :param inc2: inclination at point 2
    :param azi1: azimuth at point 1
    :param azi2: azimuth at point 2
    :param dogleg: dogleg at point 2
    :return: east coordinate at the new point (point 2)
    """
    rf = calc_rf(dogleg)
    delta_md = md2 - md1
    east_delta = 0.5 * delta_md * (sin(radians(inc1)) * sin(radians(azi1))
                                   + sin(radians(inc2)) * sin(radians(azi2))) * rf
    east_new = east_prev + east_delta

    return east_new


def calc_tvd(tvd_prev, md1, md2, inc1, inc2, dogleg):
    """
    Calculate the true vertical depth of certain point using the previous one and the minimum curvature method
    :param tvd_prev: tvd at previous point (point 1)
    :param md1: measured depth at point 1
    :param md2: measured depth at point 2
    :param inc1: inclination at point 1
    :param inc2: inclination at point 2
    :param dogleg: dogleg at point 2
    :return: tvd at the new point (point 2)
    """
    rf = calc_rf(dogleg)
    delta_md = md2 - md1
    tvd_delta = 0.5 * delta_md * (cos(radians(inc1)) + cos(radians(inc2))) * rf
    tvd_new = tvd_prev + tvd_delta

    return tvd_new


def calc_rf(dogleg):
    """
    Calculate RF for minimum curvature method
    :param dogleg: dogleg between previous and current point
    :return: RF
    """
    if dogleg == 0:
        rf = 1
    else:
        rf = tan(dogleg / 2) / (dogleg / 2)

    return rf


def calc_dls(point, delta_md, resolution=30):
    """
    Calculate dogleg severity with a defined resolution
    :param point: trajectory point
    :param delta_md: MD delta with previous point
    :param resolution: depth window to check
    :return: dls
    """

    return point['dl'] * resolution / delta_md


def interp_pt(md, trajectory):
    """
    Get an interpolated point along a trajectory, using MD as input.
    :param md: measured depth
    :param trajectory: list of survey points
    :return: an interpolated point as dict with the relevant info
    """
    
    if md < 0:
        raise ValueError('md value must be positive')
    if md > trajectory[-1]['md']:
        raise ValueError("md can't be deeper than deepest trajectory point")

    # Need to find the correct points p1 and p2 to do the interpolation
    p1 = None
    p2 = None
    for idx, point in enumerate(trajectory):
        if point['md'] < md < trajectory[idx+1]['md']:
            p1 = point
            p2 = trajectory[idx+1]
            break
        elif point['md'] == md:
            return point

    dl = (md - p1['md']) * p2['dl'] / (p2['md'] - p1['md'])
    target = {'md': md, 'dl': dl}

    if p2['sectionType'] == 'hold':
        return interp_hold(target, md, p1, p2)

    if p2['sectionType'] == 'vertical':
        return interp_vertical(target, md, p1)

    return inner_pt_calcs(target, p1, p2)


def inner_pt_calcs(inner_point, p1, p2, dl_sv=None, dls_resolution=30):
    if dl_sv is None:       # dogleg from last survey point (not interpolated)
        dl_sv = inner_point['dl']

    delta_md = inner_point['md'] - p1['md']
    inner_point['dls'] = calc_dls(inner_point, delta_md, dls_resolution)
    inner_point = get_inc_azi(inner_point, p1, p2, dl_sv)

    inner_point['north'] = calc_north(p1['north'], p1['md'],
                                      inner_point['md'],
                                      p1['inc'], inner_point['inc'],
                                      p1['azi'], inner_point['azi'],
                                      radians(inner_point['dl']))
    inner_point['east'] = calc_east(p1['east'], p1['md'],
                                    inner_point['md'],
                                    p1['inc'], inner_point['inc'],
                                    p1['azi'], inner_point['azi'],
                                    radians(inner_point['dl']))
    inner_point['tvd'] = calc_tvd(p1['tvd'], p1['md'], inner_point['md'],
                                  p1['inc'], inner_point['inc'],
                                  radians(inner_point['dl']))
    inner_point['pointType'] = 'interpolated'
    inner_point['sectionType'] = p2['sectionType']

    return inner_point


def adjust_azi(azi, azi1, azi2):
    limits = sorted([azi1, azi2])
    count = 1
    while not limits[0] <= azi <= limits[1]:
        if azi > limits[1]:
            azi -= 90
        else:
            azi += 90
        count += 1
        if count == 4:
            break
    return azi


def component(p, comp):
    if comp == 'n':
        return sin(radians(p['inc'])) * cos(radians(p['azi']))
    if comp == 'e':
        return sin(radians(p['inc'])) * sin(radians(p['azi']))
    if comp == 'v':
        return cos(radians(p['inc']))


def delta(p1, p2, dl_new, comp):
    c1 = sin(radians(p2['dl'])-radians(dl_new)) * component(p1, comp) / sin(radians(p2['dl']))
    c2 = sin(radians(dl_new)) * component(p2, comp) / sin(radians(p2['dl']))
    return c1 + c2


def get_inc_azi(p, p1, p2, dl_new):
    dn = delta(p1, p2, dl_new, 'n')
    de = delta(p1, p2, dl_new, 'e')
    dv = delta(p1, p2, dl_new, 'v')
    if p1['inc'] == p2['inc']:
        p['inc'] = p1['inc']
    else:
        p['inc'] = degrees(atan((dn**2 + de**2)**.5 / dv))
    if p1['azi'] == p2['azi']:
        p['azi'] = p1['azi']
    else:
        p['azi'] = degrees((atan(de / dn) + (2 * pi)) % (2 * pi))

    p['azi'] = adjust_azi(p['azi'], p1['azi'], p2['azi'])

    return p


def interp_hold(inner_point, md, p1, p2):
    dn = (p2['north']-p1['north']) / (p2['md'] - p1['md'])
    de = (p2['east'] - p1['east']) / (p2['md'] - p1['md'])
    dv = (p2['tvd'] - p1['tvd']) / (p2['md'] - p1['md'])
    inner_point['north'] = p1['north'] + (md - p1['md']) * dn
    inner_point['east'] = p1['east'] + (md - p1['md']) * de
    inner_point['tvd'] = p1['tvd'] + (md - p1['md']) * dv
    inner_point['pointType'] = 'interpolated'
    inner_point['sectionType'] = 'hold'

    return inner_point


def interp_vertical(inner_point, md, p1):
    inner_point['north'] = p1['north']
    inner_point['east'] = p1['east']
    inner_point['tvd'] = p1['tvd'] + (md - p1['md'])
    inner_point['pointType'] = 'interpolated'
    inner_point['sectionType'] = 'vertical'

    return inner_point
