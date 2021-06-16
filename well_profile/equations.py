from math import radians, sin, cos, acos, tan


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


def calc_dls(dogleg, md, resolution=30):
    """
    Calculate dogleg severity with a defined resolution
    :param dogleg: dogleg between previous and current point
    :param md: measured depth
    :param resolution: depth window to check
    :return: dls
    """
    dls = [0]
    for x in range(1, len(dogleg)):
        dls_new = dogleg[x] * resolution / (md[x] - md[x-1])
        dls.append(dls_new)

    return dls
