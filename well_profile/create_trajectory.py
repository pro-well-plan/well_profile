from .plot import plot_wellpath
from numpy import arange
from math import radians, sin, cos, degrees, acos
import pandas as pd


def get(mdt, grid_length=50, profile='V', build_angle=1, kop=0, eob=0, sod=0, eod=0, kop2=0, eob2=0, units='metric'):
    """
    Generate a wellpath.
    :param mdt: target depth, m or ft
    :param grid_length: cell's length, m or ft
    :param profile: 'V' for vertical, 'J' for J-type, 'S' for S-type, 'H1' for Horizontal single curve and 'H2' for
                                                                                            Horizontal double curve
    :param build_angle: building angle, °
    :param kop: kick-off point, m or ft
    :param eob: end of build, m or ft
    :param sod: start of drop, m or ft
    :param eod: end of drop, m or ft
    :param kop2: kick-off point 2, m or ft
    :param eob2: end of build 2, m or ft
    :param units: 'metric' or 'english'
    :return: a wellpath object with 3D position
    """

    deltaz = 1
    md = list(arange(0, mdt + deltaz, deltaz))  # Measured Depth from RKB, m
    zstep = len(md)  # Number of cells from RKB up to the bottom
    tvd = None
    inclination = None
    azimuth = None
    north = None
    east = None

    if profile == 'V':        # Vertical well
        tvd = md   # True Vertical Depth from RKB, m
        north = [0] * zstep  # x axis
        east = [0] * zstep  # x axis
        inclination = [0] * zstep
        azimuth = [0] * zstep

    if profile == 'J':        # J-type well
        # Vertical section
        tvd = md[:round(kop / deltaz) + 1]  # True Vertical Depth from RKB, m
        north = [0] * len(tvd)   # x axis
        east = [0] * len(tvd)   # x axis
        inclination = [0] * len(tvd)
        azimuth = [0] * len(tvd)

        # Build section
        s = deltaz
        theta_delta = radians(build_angle / round((eob - kop) / deltaz))
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

        for x in range(round((eob - kop) / deltaz)-1):
            theta += theta_delta
            inclination.append(degrees(theta))

            z_displacement = (r * sin(theta))
            tvd.append(round(z_vertical + z_displacement, 2))

            hz_displacement = r * (1 - cos(theta)) - north[-1]
            north.append(round(north[-1] + hz_displacement, 2))
            east.append(0)
            azimuth.append(0)

        # Tangent section
        z_displacement = (deltaz * cos(radians(build_angle)))
        hz_displacement = (deltaz * sin(radians(build_angle)))
        for x in range(round((mdt-eob)/deltaz)):
            tvd.append(round(tvd[-1] + z_displacement, 2))
            north.append(round(north[-1] + hz_displacement, 2))
            east.append(0)
            inclination.append(inclination[-1])
            azimuth.append(0)

    if profile == 'S':  # S-type well
        # Vertical section
        tvd = md[:round(kop / deltaz) + 1]  # True Vertical Depth from RKB, m
        north = [0] * len(tvd)  # x axis
        east = [0] * len(tvd)  # x axis
        inclination = [0] * len(tvd)
        azimuth = [0] * len(tvd)

        # Build section
        s = deltaz
        theta_delta = radians(build_angle) / round((eob - kop) / deltaz)
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

        for x in range(round((eob - kop) / deltaz) - 1):
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
        z_displacement = (deltaz * cos(radians(build_angle)))
        hz_displacement = (deltaz * sin(radians(build_angle)))

        for x in range(round((sod - eob) / deltaz)):
            tvd.append(round(tvd[-1] + z_displacement, 2))
            north.append(round(north[-1] + hz_displacement, 2))
            east.append(0)
            inclination.append(inclination[-1])
            azimuth.append(0)

        # Drop section
        s = deltaz
        cells_drop = round((eod - sod) / deltaz)
        theta_delta = radians(build_angle) / cells_drop
        theta = radians(build_angle)
        r = s / theta_delta
        z_checkpoint = tvd[-1]
        hz_checkpoint = north[-1]
        for x in range(cells_drop):
            z_displacement = r * (sin(theta) - sin(theta - (theta_delta * (x + 1))))
            tvd.append(round(z_checkpoint + z_displacement, 2))

            hz_displacement = r * (1 - cos(theta)) - r * (1 - cos(theta - (theta_delta * (x + 1))))
            north.append(round(hz_checkpoint + hz_displacement, 2))
            east.append(0)
            inclination.append(inclination[-1] - degrees(theta_delta))
            azimuth.append(0)

        # Vertical section
        for x in range(round((mdt - eod) / deltaz)):
            tvd.append(round(tvd[-1] + deltaz, 2))
            north.append(north[-1])  # x axis
            east.append(0)
            inclination.append(0)
            azimuth.append(0)

    if profile == 'H1':        # Horizontal single-curve well
        # Vertical section
        tvd = md[:round(kop / deltaz) + 1]  # True Vertical Depth from RKB, m
        north = [0] * len(tvd)  # x axis
        east = [0] * len(tvd)  # x axis
        inclination = [0] * len(tvd)
        azimuth = [0] * len(tvd)

        # Build section
        s = deltaz
        theta_delta = radians(90) / round((eob - kop) / deltaz)
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

        for x in range(round((eob - kop) / deltaz)-1):
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
        for x in range(round((mdt-eob)/deltaz)):
            tvd.append(tvd[-1])
            north.append(north[-1] + deltaz)
            east.append(0)
            inclination.append(90)
            azimuth.append(0)

    if profile == 'H2':        # Horizontal double-curve well
        # Vertical section
        tvd = md[:round(kop / deltaz) + 1]  # True Vertical Depth from RKB, m
        north = [0] * len(tvd)  # x axis
        east = [0] * len(tvd)  # x axis
        inclination = [0] * len(tvd)
        azimuth = [0] * len(tvd)

        # Build section
        s = deltaz
        theta_delta = radians(build_angle / round((eob - kop) / deltaz))
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

        for x in range(round((eob - kop) / deltaz)-1):
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
        z_displacement = (deltaz * cos(radians(build_angle)))
        hz_displacement = (deltaz * sin(radians(build_angle)))
        for x in range(round((kop2-eob)/deltaz)):
            tvd.append(round(tvd[-1] + z_displacement, 2))
            inclination.append(inclination[-1])
            north.append(round(north[-1] + hz_displacement, 2))
            east.append(0)
            azimuth.append(0)

        # Build section 2
        s = deltaz
        build_angle = 90 - build_angle
        cells_drop = round((eob2 - kop2) / deltaz)
        theta_delta = radians(build_angle) / cells_drop
        theta = radians(build_angle)
        r = s / theta_delta
        z_checkpoint = tvd[-1]
        hz_checkpoint = north[-1]

        for x in range(cells_drop):
            hz_displacement = r * (sin(theta) - sin(theta - (theta_delta * (x + 1))))
            north.append(round(hz_checkpoint + hz_displacement, 2))
            inclination.append(inclination[-1] + degrees(theta_delta))
            east.append(0)
            azimuth.append(0)

            z_displacement = r * (1 - cos(theta)) - r * (1 - cos(theta - (theta_delta * (x + 1))))
            tvd.append(round(z_checkpoint + z_displacement, 2))

        # Horizontal section
        for x in range(round((mdt - eob2) / deltaz)):
            tvd.append(tvd[-1])
            north.append(north[-1] + deltaz)
            inclination.append(inclination[-1])
            east.append(0)
            azimuth.append(0)

    # Defining type of section
    sections = ['vertical', 'vertical']
    for z in range(2, len(tvd)):
        delta_tvd = round(tvd[z] - tvd[z - 1], 9)
        if inclination[z] == 0:  # Vertical Section
            sections.append('vertical')
        else:
            if round(inclination[z], 2) == round(inclination[z - 1], 2):
                if delta_tvd == 0:
                    sections.append('horizontal')  # Horizontal Section
                else:
                    sections.append('hold')  # Straight Inclined Section
            else:
                if inclination[z] > inclination[z - 1]:  # Built-up Section
                    sections.append('build-up')
                if inclination[z] < inclination[z - 1]:  # Drop-off Section
                    sections.append('drop-off')

    md = md[0::grid_length]
    tvd = tvd[0::grid_length]
    north = north[0::grid_length]
    east = east[0::grid_length]
    inclination = inclination[0::grid_length]
    azimuth = azimuth[0::grid_length]
    sections = sections[0::grid_length]

    dogleg = [0]
    inc = inclination.copy()
    for x in range(1, len(md)):
        dogleg.append(acos(
            cos(radians(inc[x])) * cos(radians(inc[x - 1]))
            - sin(radians(inc[x])) * sin(radians(inc[x - 1])) * (1 - cos(radians(azimuth[x] - azimuth[x - 1])))
        ))
    dogleg = [degrees(x) for x in dogleg]

    class WellDepths(object):
        def __init__(self):
            self.md = md
            self.tvd = tvd
            self.deltaz = grid_length
            self.zstep = len(md)
            self.north = north
            self.east = east
            self.inclination = [round(i, 2) for i in inclination]
            self.dogleg = dogleg
            self.azimuth = azimuth
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

    return WellDepths()
