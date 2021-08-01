from unittest import TestCase
from well_profile import load


class TestLoadTrajectory(TestCase):

    def test_get_point(self):
        well = load(r'https://github.com/pro-well-plan/well_profile/raw/master/well_profile/tests/trajectory1.xlsx')

        with self.assertRaises(ValueError):
            well.get_point(-10)

        self.assertTrue(all([i in well.get_point(0).keys() for i in ['md', 'inc', 'azi', 'north', 'east', 'tvd',
                                                                     'dl']]))
        self.assertTrue(all([i in well.get_point(2000).keys() for i in ['md', 'inc', 'azi', 'north', 'east', 'tvd',
                                                                        'dl']]))
        self.assertTrue(all([i in well.get_point(3790).keys() for i in ['md', 'inc', 'azi', 'north', 'east', 'tvd',
                                                                        'dl']]))

        with self.assertRaises(ValueError):
            well.get_point(4000)

        # getting two survey points
        p1 = well.get_point(3722.9)
        p2 = well.get_point(3761.8)
        self.assertTrue(p1['pointType'] == p2['pointType'] == 'survey')
        # interpolate between p1 and p2
        p12 = well.get_point(3750)
        self.assertTrue(p12['md'] == 3750)
        self.assertTrue(p2['inc'] <= p12['inc'] <= p1['inc'])       # p1['inc'] >= p2['inc']
        self.assertTrue(p1['azi'] == p12['azi'] == p2['azi'])       # constant azi for this section
        self.assertTrue(p12['dl'] < p2['dl'])

        run_assertions(self, well, 3790)


def run_assertions(obj, well, mdt):
    traj = well.trajectory
    obj.assertIsInstance(well.npoints, int, msg='points is not an integer')
    obj.assertEqual(traj[-1]['md'], mdt, msg='Target depth not reached')
    obj.assertEqual(traj[0]['md'], traj[0]['tvd'], msg='MD and TVD are different at first cell')
    obj.assertIn('pointType', traj[0], msg='pointType property was not found for first trajectory point')
