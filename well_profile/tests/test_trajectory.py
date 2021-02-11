from unittest import TestCase
from well_profile import get, load
import pandas as pd


class TestCreate(TestCase):

    def test_get(self):

        profile = ['V', 'J', 'S', 'H1', 'H2']

        for x in profile:
            my_wp = get(100, cells_no=100, profile=x, build_angle=45, kop=20, eob=40, sod=60, eod=80,
                        kop2=60, eob2=80)

            run_assertions(self, my_wp, 100)

    def test_load_from_excel(self):
        my_wp = load(r'https://github.com/pro-well-plan/well_profile/raw/master/well_profile/tests/trajectory1.xlsx')

        run_assertions(self, my_wp, 3790)

    def test_load_from_df(self):

        df = pd.read_excel(r'https://github.com/pro-well-plan/well_profile/raw/master/well_profile/tests/'
                           r'trajectory1.xlsx')
        my_wp = load(df)

        run_assertions(self, my_wp, 3790)

    def test_load_from_dicts(self):

        data = [{'md': 0, 'tvd': 0, 'azimuth': 0, 'inclination': 0},
                {'md': 1, 'tvd': 1, 'azimuth': 0, 'inclination': 0},
                {'md': 2, 'tvd': 2, 'azimuth': 0, 'inclination': 0},
                {'md': 3, 'tvd': 3, 'azimuth': 0, 'inclination': 0},
                {'md': 4, 'tvd': 4, 'azimuth': 0, 'inclination': 0},
                {'md': 5, 'tvd': 5, 'azimuth': 0, 'inclination': 0},
                ]

        my_wp = load(data, cells_no=100)

        run_assertions(self, my_wp, 5)

    def test_load_from_lists(self):

        data = [[0, 1, 2, 3, 4, 5],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 1, 2, 3, 4, 5]]

        my_wp = load(data, cells_no=100)

        run_assertions(self, my_wp, 5)

    def test_load_df(self):

        my_wp = load(load(r'https://github.com/pro-well-plan/well_profile/raw/master/well_profile/tests/'
                          r'trajectory1.xlsx').df())

        run_assertions(self, my_wp, 3790)

    def test_load_initial(self):

        my_wp = load(r'https://github.com/pro-well-plan/well_profile/raw/master/well_profile/tests/trajectory1.xlsx')
        my_wp_initial = my_wp._base_data

        self.assertIsInstance(my_wp, object, msg='main function is not returning an object')
        self.assertIsInstance(my_wp_initial, pd.DataFrame, msg='method is not returning a dataframe')


def run_assertions(self, my_wp, mdt):
    traj = my_wp.trajectory
    self.assertIsInstance(my_wp.cells_no, int, msg='cells_no is not an integer')
    self.assertEqual(traj[-1]['md'], mdt, msg='Target depth not reached')
    self.assertEqual(traj[0]['md'], traj[0]['tvd'], msg='MD and TVD are different at first cell')
    self.assertEqual(my_wp.cells_no, len(traj), msg='Number of cells is not correct')
