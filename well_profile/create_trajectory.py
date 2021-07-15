from .equations import *
from numpy import arange
from math import degrees
from .well import Well, define_section


def get(mdt, profile='V', build_angle=1, kop=0, eob=0, sod=0, eod=0, kop2=0, eob2=0, **kwargs):
    """
    Generate a wellpath.

    Parameters
    ----------
    mdt: num
        target depth, m or ft
    profile: str
        'V' for vertical, 'J' for J-type, 'S' for S-type, 'H1' for Horizontal single curve and 'H2' for Horizontal double curve
    build_angle: num
        building angle, °
    kop: num
        kick-off point, m or ft
    eob: num
        end of build, m or ft
    sod: num
        start of drop, m or ft
    eod: num
        end of drop, m or ft
    kop2: num
        kick-off point 2, m or ft
    eob2: num
        end of build 2, m or ft

    Keyword Args
    ------------
    points: int
        number of points
    set_start: dict, None
        set initial point in m {'north': 0, 'east': 0}.
    change_azimuth: float, int, None
        add specific degrees to azimuth values along the entire well.
    set_info: dict, None
        dict, {'dlsResolution', 'wellType': 'onshore'|'offshore', 'units': 'metric'|'english'}.

    Returns
    -------
    well: well object
        A wellpath object with 3D position
    """

    # Settings
    params = {'points': 100, 'set_start': None, 'change_azimuth': None, 'set_info': None, 'ndigits': 2}
    for key, value in kwargs.items():
        params[key] = value
    set_start = params['set_start']
    change_azimuth = params['change_azimuth']
    set_info = params['set_info']

    info = {'dlsResolution': 30, 'wellType': 'offshore', 'units': 'metric'}

    initial_point = {'north': 0, 'east': 0, 'depth': 0}

    if isinstance(set_info, dict):
        for param in set_info:  # changing default values
            if param in info:
                info[param] = set_info[param]

    if isinstance(set_start, dict):
        for x in set_start:  # changing default values
            if x in initial_point:
                initial_point[x] = set_start[x]

    md = list(arange(0, mdt + 1, 1))    # Measured Depth from RKB, m
    depth_step = md[1]

    if profile == 'V':        # Vertical well
        tvd, north, east, inc, az = vertical_section(profile, md, kop, depth_step)

    elif profile == 'J':        # J-type well
        tvd, north, east, inc, az = create_j_well(mdt, md, kop, eob, build_angle, depth_step)

    elif profile == 'S':  # S-type well
        tvd, north, east, inc, az = create_s_well(mdt, md, kop, eob, sod, eod, build_angle, depth_step)

    elif profile == 'H1':     # Horizontal single-curve well
        tvd, north, east, inc, az = create_h1_well(mdt, md, kop, eob, depth_step)

    else:        # Horizontal double-curve well
        tvd, north, east, inc, az = create_h2_well(mdt, md, kop, eob, kop2, eob2, build_angle, depth_step)

    if change_azimuth is not None:
        az, north_new, east_new = mod_azimuth(change_azimuth, az, north, east)

    # CREATING TRAJECTORY POINTS
    trajectory = [{'md': 0, 'inc': 0, 'azi': 0, 'dl': 0, 'tvd': 0, 'sectionType': 'vertical'}]
    trajectory[-1].update(initial_point)
    for idx, md in enumerate(md):
        if idx > 0:
            dogleg = calc_dogleg(inc[idx - 1], inc[idx], az[idx - 1], az[idx])
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
                     'dl': degrees(dogleg)
                     }
            point['sectionType'] = define_section(point, trajectory[-1])
            trajectory.append(point)

    return Well({'trajectory': trajectory, 'info': info})


def vertical_section(profile, md, kop, depth_step):
    if profile == 'V':
        tvd = md
    else:
        tvd = md[:round(kop / depth_step) + 1]  # True Vertical Depth from RKB, m

    north = [0] * len(tvd)  # x axis
    east = [0] * len(tvd)  # x axis
    inclination = [0.0] * len(tvd)
    azimuth = [0] * len(tvd)

    return tvd, north, east, inclination, azimuth


def create_s_well(mdt, md, kop, eob, sod, eod, build_angle, depth_step):
    # Vertical section
    tvd, north, east, inclination, azimuth = vertical_section('S', md, kop, depth_step)

    # Build section
    s = depth_step
    theta_delta = radians(build_angle) / round((eob - kop) / depth_step)
    theta = theta_delta
    r = s / theta

    z_displacement = (r * sin(theta))
    tvd.append(round(tvd[-1] + z_displacement, 2))
    z_count = z_displacement

    hz_displacement = r * (1 - cos(theta))
    north.append(round(north[-1] + hz_displacement, 2))
    east.append(0)
    inclination.append(degrees(theta))
    azimuth.append(0)

    for x in range(round((eob - kop) / depth_step) - 1):
        theta += theta_delta
        inclination.append(degrees(theta))
        z_displacement = (r * sin(theta)) - z_count
        tvd.append(round(tvd[-1] + z_displacement, 2))
        z_count += z_displacement

        hz_displacement = r * (1 - cos(theta)) - north[-1]
        north.append(round(north[-1] + hz_displacement, 2))
        east.append(0)
        azimuth.append(0)

    # Tangent section
    z_displacement = (depth_step * cos(radians(build_angle)))
    hz_displacement = (depth_step * sin(radians(build_angle)))

    for x in range(round((sod - eob) / depth_step)):
        tvd.append(round(tvd[-1] + z_displacement, 2))
        north.append(round(north[-1] + hz_displacement, 2))
        east.append(0)
        inclination.append(inclination[-1])
        azimuth.append(0)

    # Drop section
    s = depth_step
    points_drop = round((eod - sod) / depth_step)
    theta_delta = radians(build_angle) / points_drop
    theta = radians(build_angle)
    r = s / theta_delta
    z_checkpoint = tvd[-1]
    hz_checkpoint = north[-1]
    for x in range(points_drop):
        z_displacement = r * (sin(theta) - sin(theta - (theta_delta * (x + 1))))
        tvd.append(round(z_checkpoint + z_displacement, 2))

        hz_displacement = r * (1 - cos(theta)) - r * (1 - cos(theta - (theta_delta * (x + 1))))
        north.append(round(hz_checkpoint + hz_displacement, 2))
        east.append(0)
        inclination.append(inclination[-1] - degrees(theta_delta))
        azimuth.append(0)

    # Vertical section
    for x in range(round((mdt - eod) / depth_step)):
        tvd.append(round(tvd[-1] + depth_step, 2))
        north.append(north[-1])  # x axis
        east.append(0)
        inclination.append(0)
        azimuth.append(0)

    return tvd, north, east, inclination, azimuth


def create_j_well(mdt, md, kop, eob, build_angle, depth_step):
    # Vertical section
    tvd, north, east, inclination, azimuth = vertical_section('J', md, kop, depth_step)

    # Build section
    s = depth_step
    theta_delta = radians(build_angle / round((eob - kop) / depth_step))
    theta = theta_delta
    r = s / theta

    z_vertical = tvd[-1]
    z_displacement = (r * sin(theta))
    tvd.append(round(tvd[-1] + z_displacement, 2))

    hz_displacement = r * (1 - cos(theta))
    north.append(round(north[-1] + hz_displacement, 2))
    east.append(0)
    inclination.append(degrees(theta))
    azimuth.append(0)

    for x in range(round((eob - kop) / depth_step) - 1):
        theta += theta_delta
        inclination.append(degrees(theta))

        z_displacement = (r * sin(theta))
        tvd.append(round(z_vertical + z_displacement, 2))

        hz_displacement = r * (1 - cos(theta)) - north[-1]
        north.append(round(north[-1] + hz_displacement, 2))
        east.append(0)
        azimuth.append(0)

    # Tangent section
    z_displacement = (depth_step * cos(radians(build_angle)))
    hz_displacement = (depth_step * sin(radians(build_angle)))
    for x in range(round((mdt - eob) / depth_step)):
        tvd.append(round(tvd[-1] + z_displacement, 2))
        north.append(round(north[-1] + hz_displacement, 2))
        east.append(0)
        inclination.append(inclination[-1])
        azimuth.append(0)

    return tvd, north, east, inclination, azimuth


def create_h1_well(mdt, md, kop, eob, depth_step):
    # Vertical section
    tvd, north, east, inclination, azimuth = vertical_section('H1', md, kop, depth_step)

    # Build section
    s = depth_step
    theta_delta = radians(90) / round((eob - kop) / depth_step)
    theta = theta_delta
    r = s / theta

    z_displacement = (r * sin(theta))
    tvd.append(round(tvd[-1] + z_displacement, 2))
    z_count = z_displacement

    hz_displacement = r * (1 - cos(theta))
    north.append(round(north[-1] + hz_displacement, 2))
    east.append(0)
    inclination.append(degrees(theta))
    azimuth.append(0)

    for x in range(round((eob - kop) / depth_step) - 1):
        theta += theta_delta
        z_displacement = (r * sin(theta)) - z_count
        tvd.append(round(tvd[-1] + z_displacement, 2))
        z_count += z_displacement

        hz_displacement = r * (1 - cos(theta)) - north[-1]
        inclination.append(degrees(theta))
        north.append(round(north[-1] + hz_displacement, 2))
        east.append(0)
        azimuth.append(0)

    # Horizontal section
    for x in range(round((mdt - eob) / depth_step)):
        tvd.append(tvd[-1])
        north.append(north[-1] + depth_step)
        east.append(0)
        inclination.append(90)
        azimuth.append(0)

    return tvd, north, east, inclination, azimuth


def create_h2_well(mdt, md, kop, eob, kop2, eob2, build_angle, depth_step):
    # Vertical section
    tvd, north, east, inclination, azimuth = vertical_section('H2', md, kop, depth_step)

    # Build section
    s = depth_step
    theta_delta = radians(build_angle / round((eob - kop) / depth_step))
    theta = theta_delta
    r = s / theta

    z_displacement = (r * sin(theta))
    tvd.append(round(tvd[-1] + z_displacement, 2))
    z_count = z_displacement

    hz_displacement = r * (1 - cos(theta))
    north.append(round(north[-1] + hz_displacement, 2))
    east.append(0)
    inclination.append(degrees(theta))
    azimuth.append(0)

    for x in range(round((eob - kop) / depth_step) - 1):
        theta = theta + theta_delta
        z_displacement = (r * sin(theta)) - z_count
        tvd.append(round(tvd[-1] + z_displacement, 2))
        z_count += z_displacement

        hz_displacement = r * (1 - cos(theta)) - north[-1]
        inclination.append(degrees(theta))
        north.append(round(north[-1] + hz_displacement, 2))
        east.append(0)
        azimuth.append(0)

    # Tangent section
    z_displacement = (depth_step * cos(radians(build_angle)))
    hz_displacement = (depth_step * sin(radians(build_angle)))
    for x in range(round((kop2 - eob) / depth_step)):
        tvd.append(round(tvd[-1] + z_displacement, 2))
        inclination.append(inclination[-1])
        north.append(round(north[-1] + hz_displacement, 2))
        east.append(0)
        azimuth.append(0)

    # Build section 2
    s = depth_step
    build_angle = 90 - build_angle
    points_drop = round((eob2 - kop2) / depth_step)
    theta_delta = radians(build_angle) / points_drop
    theta = radians(build_angle)
    r = s / theta_delta
    z_checkpoint = tvd[-1]
    hz_checkpoint = north[-1]

    for x in range(points_drop):
        hz_displacement = r * (sin(theta) - sin(theta - (theta_delta * (x + 1))))
        north.append(round(hz_checkpoint + hz_displacement, 2))
        inclination.append(inclination[-1] + degrees(theta_delta))
        east.append(0)
        azimuth.append(0)

        z_displacement = r * (1 - cos(theta)) - r * (1 - cos(theta - (theta_delta * (x + 1))))
        tvd.append(round(z_checkpoint + z_displacement, 2))

    # Horizontal section
    for x in range(round((mdt - eob2) / depth_step)):
        tvd.append(tvd[-1])
        north.append(north[-1] + depth_step)
        inclination.append(inclination[-1])
        east.append(0)
        azimuth.append(0)

    return tvd, north, east, inclination, azimuth


def mod_azimuth(change_azimuth, azimuth_new, north_new, east_new):
    for a in range(len(azimuth_new)):
        azimuth_new[a] += change_azimuth

        if change_azimuth <= 90:
            east_new[a] = north_new[a] * sin(radians(change_azimuth))
            north_new[a] *= cos(radians(change_azimuth))
        elif 90 < change_azimuth <= 180:
            angle = change_azimuth - 90
            east_new[a] = north_new[a] * round(cos(radians(angle)), 3)
            north_new[a] *= - sin(radians(angle))
        elif 180 < change_azimuth <= 270:
            angle = change_azimuth - 180
            east_new[a] = - north_new[a] * round(sin(radians(angle)), 3)
            north_new[a] *= - cos(radians(angle))
        else:
            angle = change_azimuth - 270
            east_new[a] = - north_new[a] * round(cos(radians(angle)), 3)
            north_new[a] *= sin(radians(angle))

    return azimuth_new, north_new, east_new
