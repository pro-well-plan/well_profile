from unittest import TestCase
from well_profile import get, load, two_points
import pandas as pd


class TestCreate(TestCase):

    def test_get(self):

        profile = ['V', 'J', 'S', 'H1', 'H2']

        for x in profile:
            well = get(100, points=100, profile=x, build_angle=45, kop=20, eob=40, sod=60, eod=80,
                       kop2=60, eob2=80)

            run_assertions(self, well, 100)

    def test_load_from_excel(self):
        well = load(r'https://github.com/pro-well-plan/well_profile/raw/master/well_profile/tests/trajectory1.xlsx')

        run_assertions(self, well, 3790)

    def test_load_from_df(self):

        df = pd.read_excel(r'https://github.com/pro-well-plan/well_profile/raw/master/well_profile/tests/'
                           r'trajectory1.xlsx')
        well = load(df)

        run_assertions(self, well, 3790)

    def test_load_from_dicts(self):

        data = [{'md': 0, 'tvd': 0, 'azimuth': 0, 'inclination': 0},
                {'md': 1, 'tvd': 1, 'azimuth': 0, 'inclination': 0},
                {'md': 2, 'tvd': 2, 'azimuth': 0, 'inclination': 0},
                {'md': 3, 'tvd': 3, 'azimuth': 0, 'inclination': 0},
                {'md': 4, 'tvd': 4, 'azimuth': 0, 'inclination': 0},
                {'md': 5, 'tvd': 5, 'azimuth': 0, 'inclination': 0},
                ]

        well = load(data, points=100)

        run_assertions(self, well, 5)

    def test_load_from_lists(self):

        data = [[0, 1, 2, 3, 4, 5],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 1, 2, 3, 4, 5]]

        well = load(data, points=100)

        run_assertions(self, well, 5)

    def test_load_df(self):

        well = load(load(r'https://github.com/pro-well-plan/well_profile/raw/master/well_profile/tests/'
                         r'trajectory1.xlsx').df())

        run_assertions(self, well, 3790)

    def test_load_initial(self):

        well = load(r'https://github.com/pro-well-plan/well_profile/raw/master/well_profile/tests/trajectory1.xlsx')
        well_initial = well._base_data

        self.assertIsInstance(well, object, msg='main function is not returning an object')
        self.assertIsInstance(well_initial, pd.DataFrame, msg='method is not returning a dataframe')

    def test_gen_two_points_case1(self):
        # change in vertical = change in horizontal
        point_1 = {'north': 0, 'east': 0, 'tvd': 300}
        point_2 = {'north': 0, 'east': -500, 'tvd': 800}

        well = two_points({'kickoff': point_1, 'target': point_2})
        self.assertEqual(well.trajectory[-1]['north'], point_2['north'], msg='Getting wrong north at TD')
        self.assertEqual(well.trajectory[-1]['east'], point_2['east'], msg='Getting wrong east at TD')

        run_assertions(self, well, well.trajectory[-1]['md'])

    def test_gen_two_points_case2(self):
        # change in vertical < change in horizontal
        point_1 = {'north': 0, 'east': 0, 'tvd': 300}
        point_2 = {'north': -100, 'east': 800, 'tvd': 800}

        well = two_points({'kickoff': point_1, 'target': point_2})
        self.assertEqual(well.trajectory[-1]['north'], point_2['north'], msg='Getting wrong north at TD')
        self.assertEqual(well.trajectory[-1]['east'], point_2['east'], msg='Getting wrong east at TD')

        run_assertions(self, well, well.trajectory[-1]['md'])

    def test_gen_two_points_case3(self):
        # change in vertical > change in horizontal
        point_1 = {'north': 0, 'east': 0, 'tvd': 300}
        point_2 = {'north': 500, 'east': 0, 'tvd': 1900}

        well = two_points({'kickoff': point_1, 'target': point_2})
        self.assertEqual(well.trajectory[-1]['north'], point_2['north'], msg='Getting wrong north at TD')
        self.assertEqual(well.trajectory[-1]['east'], point_2['east'], msg='Getting wrong east at TD')

        run_assertions(self, well, well.trajectory[-1]['md'])


def run_assertions(self, well, mdt):
    traj = well.trajectory
    self.assertIsInstance(well.points, int, msg='points is not an integer')
    self.assertEqual(traj[-1]['md'], mdt, msg='Target depth not reached')
    self.assertEqual(traj[0]['md'], traj[0]['tvd'], msg='MD and TVD are different at first cell')
    self.assertEqual(well.points, len(traj), msg='Number of points is not correct')
