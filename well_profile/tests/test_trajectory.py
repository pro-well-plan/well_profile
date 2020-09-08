from unittest import TestCase
import well_profile as wp
import pandas as pd


class TestCreate(TestCase):

    def test_get(self):

        profile = ['V', 'J', 'S', 'H1', 'H2']

        for x in profile:

            my_wp = wp.get(100, grid_length=1, profile=x, build_angle=45, kop=20, eob=40, sod=60, eod=80,
                           kop2=60, eob2=80)

            self.assertIsInstance(my_wp.zstep, int, msg='zstep is not an integer')
            self.assertEqual(my_wp.md[0], 0, msg='MD is not starting from 0')
            self.assertEqual(my_wp.md[-1], 100, msg='Target depth not reached')
            self.assertEqual(my_wp.zstep, len(my_wp.tvd), msg='wrong number of values in tvd')
            self.assertEqual(my_wp.zstep, len(my_wp.north), msg='wrong number of values in north')
            self.assertEqual(my_wp.zstep, len(my_wp.east), msg='wrong number of values in east')
            self.assertEqual(my_wp.zstep, len(my_wp.inclination), msg='wrong number of values in inclination')
            self.assertEqual(my_wp.zstep, len(my_wp.dogleg), msg='wrong number of values in dogleg')
            self.assertEqual(my_wp.zstep, len(my_wp.azimuth), msg='wrong number of values in azimuth')
            self.assertIsInstance(my_wp.deltaz, int, msg='grid length is not an integer')

    def test_load_from_excel(self):

        my_wp = wp.load('trajectory1.xlsx')

        self.assertIsInstance(my_wp.zstep, int, msg='zstep is not an integer')
        self.assertEqual(my_wp.md[0], 0, msg='MD is not starting from 0')
        self.assertEqual(my_wp.zstep, len(my_wp.tvd), msg='wrong number of values in tvd')
        self.assertEqual(my_wp.zstep, len(my_wp.north), msg='wrong number of values in north')
        self.assertEqual(my_wp.zstep, len(my_wp.east), msg='wrong number of values in east')
        self.assertEqual(my_wp.zstep, len(my_wp.inclination), msg='wrong number of values in inclination')
        self.assertEqual(my_wp.zstep, len(my_wp.dogleg), msg='wrong number of values in dogleg')
        self.assertEqual(my_wp.zstep, len(my_wp.azimuth), msg='wrong number of values in azimuth')
        self.assertIsInstance(my_wp.deltaz, int, msg='grid length is not an integer')

    def test_load_from_df(self):

        df = pd.read_excel('trajectory1.xlsx')
        my_wp = wp.load(df)

        self.assertIsInstance(my_wp.zstep, int, msg='zstep is not an integer')
        self.assertEqual(my_wp.md[0], 0, msg='MD is not starting from 0')
        self.assertEqual(my_wp.zstep, len(my_wp.tvd), msg='wrong number of values in tvd')
        self.assertEqual(my_wp.zstep, len(my_wp.north), msg='wrong number of values in north')
        self.assertEqual(my_wp.zstep, len(my_wp.east), msg='wrong number of values in east')
        self.assertEqual(my_wp.zstep, len(my_wp.inclination), msg='wrong number of values in inclination')
        self.assertEqual(my_wp.zstep, len(my_wp.dogleg), msg='wrong number of values in dogleg')
        self.assertEqual(my_wp.zstep, len(my_wp.azimuth), msg='wrong number of values in azimuth')
        self.assertIsInstance(my_wp.deltaz, int, msg='grid length is not an integer')

    def test_load_from_data(self):

        data = [{'md': 0, 'tvd': 0, 'azimuth': 0, 'inclination': 0},
                {'md': 1, 'tvd': 1, 'azimuth': 0, 'inclination': 0},
                {'md': 2, 'tvd': 2, 'azimuth': 0, 'inclination': 0},
                {'md': 3, 'tvd': 3, 'azimuth': 0, 'inclination': 0},
                {'md': 4, 'tvd': 4, 'azimuth': 0, 'inclination': 0},
                {'md': 5, 'tvd': 5, 'azimuth': 0, 'inclination': 0},
                ]

        my_wp = wp.load(data, grid_length=1)

        self.assertIsInstance(my_wp.zstep, int, msg='zstep is not an integer')
        self.assertEqual(my_wp.md[0], 0, msg='MD is not starting from 0')
        self.assertEqual(my_wp.md[-1], 5, msg='Target depth not reached')
        self.assertEqual(my_wp.zstep, len(my_wp.tvd), msg='wrong number of values in tvd')
        self.assertEqual(my_wp.zstep, len(my_wp.north), msg='wrong number of values in north')
        self.assertEqual(my_wp.zstep, len(my_wp.east), msg='wrong number of values in east')
        self.assertEqual(my_wp.zstep, len(my_wp.inclination), msg='wrong number of values in inclination')
        self.assertEqual(my_wp.zstep, len(my_wp.dogleg), msg='wrong number of values in dogleg')
        self.assertEqual(my_wp.zstep, len(my_wp.azimuth), msg='wrong number of values in azimuth')
        self.assertIsInstance(my_wp.deltaz, int, msg='grid length is not an integer')

    def test_load_df(self):

        my_wp = wp.load('trajectory1.xlsx').df()

        self.assertIsInstance(my_wp, pd.DataFrame, msg='method is not returning a dataframe')
        self.assertEqual(len(my_wp.md), len(my_wp.tvd), msg='wrong number of values in tvd')
        self.assertEqual(len(my_wp.md), len(my_wp.north), msg='wrong number of values in north')
        self.assertEqual(len(my_wp.md), len(my_wp.east), msg='wrong number of values in east')
        self.assertEqual(len(my_wp.md), len(my_wp.inclination), msg='wrong number of values in inclination')
        self.assertEqual(len(my_wp.md), len(my_wp.azimuth), msg='wrong number of values in azimuth')

    def test_load_initial(self):

        my_wp = wp.load('trajectory1.xlsx')
        my_wp_initial = my_wp.initial()

        self.assertIsInstance(my_wp, object, msg='main function is not returning an object')
        self.assertIsInstance(my_wp_initial, pd.DataFrame, msg='method is not returning a dataframe')

