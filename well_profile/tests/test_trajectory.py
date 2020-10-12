from unittest import TestCase
from well_profile import get, load
import pandas as pd


class TestCreate(TestCase):

    def test_get(self):

        profile = ['V', 'J', 'S', 'H1', 'H2']

        for x in profile:
            my_wp = get(100, cells_no=100, profile=x, build_angle=45, kop=20, eob=40, sod=60, eod=80,
                        kop2=60, eob2=80)
            print(my_wp.depth_step)
            run_assertions(self, my_wp, 100)

    def test_load_from_excel(self):

        my_wp = load('trajectory1.xlsx')

        run_assertions(self, my_wp, 3790)

    def test_load_from_df(self):

        df = pd.read_excel('trajectory1.xlsx')
        my_wp = load(df)

        run_assertions(self, my_wp, 3790)

    def test_load_from_data(self):

        data = [{'md': 0, 'tvd': 0, 'azimuth': 0, 'inclination': 0},
                {'md': 1, 'tvd': 1, 'azimuth': 0, 'inclination': 0},
                {'md': 2, 'tvd': 2, 'azimuth': 0, 'inclination': 0},
                {'md': 3, 'tvd': 3, 'azimuth': 0, 'inclination': 0},
                {'md': 4, 'tvd': 4, 'azimuth': 0, 'inclination': 0},
                {'md': 5, 'tvd': 5, 'azimuth': 0, 'inclination': 0},
                ]

        my_wp = load(data, cells_no=100)

        run_assertions(self, my_wp, 5)

    def test_load_df(self):

        my_wp = load(load('trajectory1.xlsx').df())

        run_assertions(self, my_wp, 3790)

    def test_load_initial(self):

        my_wp = load('trajectory1.xlsx')
        my_wp_initial = my_wp.initial()

        self.assertIsInstance(my_wp, object, msg='main function is not returning an object')
        self.assertIsInstance(my_wp_initial, pd.DataFrame, msg='method is not returning a dataframe')


def run_assertions(self, my_wp, mdt):
    self.assertIsInstance(my_wp.cells_no, int, msg='cells_no is not an integer')
    self.assertEqual(my_wp.md[-1], mdt, msg='Target depth not reached')
    self.assertEqual(my_wp.md[0], my_wp.tvd[0], msg='MD and TVD are different at first cell')
    self.assertEqual(len(my_wp.md), len(my_wp.tvd), msg='wrong number of values in tvd')
    self.assertEqual(len(my_wp.md), len(my_wp.north), msg='wrong number of values in north')
    self.assertEqual(len(my_wp.md), len(my_wp.east), msg='wrong number of values in east')
    self.assertEqual(len(my_wp.md), len(my_wp.inclination), msg='wrong number of values in inclination')
    self.assertEqual(my_wp.cells_no, len(my_wp.dogleg), msg='wrong number of values in dogleg')
    self.assertEqual(len(my_wp.md), len(my_wp.azimuth), msg='wrong number of values in azimuth')
    self.assertEqual(my_wp.md[1] - my_wp.md[0], my_wp.depth_step, msg='wrong value for depth step')
