from unittest import TestCase
from well_profile import load


class TestLoadTrajectory(TestCase):

    def test_get_point(self):
        well = load(r'https://github.com/pro-well-plan/well_profile/raw/master/well_profile/tests/trajectory1.xlsx')

        self.assertTrue(all([i in well.get_point(0).keys() for i in ['md', 'inc', 'azi', 'north', 'east', 'tvd',
                                                                     'dl', 'dls']]))
        self.assertTrue(all([i in well.get_point(2000).keys() for i in ['md', 'inc', 'azi', 'north', 'east', 'tvd',
                                                                        'dl', 'dls']]))
        self.assertTrue(all([i in well.get_point(3790).keys() for i in ['md', 'inc', 'azi', 'north', 'east', 'tvd',
                                                                        'dl', 'dls']]))

        with self.assertRaises(ValueError):         # raising error for negative depth
            well.get_point(-10)

        with self.assertRaises(ValueError):         # raising error for deeper point than trajectory length
            well.get_point(4000)

        # interpolating vertical section
        p = well.get_point(100)
        self.assertTrue(p == {'md': 100, 'dl': 0.0, 'dls': 0, 'north': 0, 'east': 0, 'tvd': 100,
                              'inc': 0, 'azi': 0,
                              'pointType': 'interpolated', 'sectionType': 'vertical'})
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
        self.assertTrue((p12['dls'] == p2['dls']))

        run_assertions(self, well, 3790)

    def test_get_point_tvd(self):
        well = load(r'https://github.com/pro-well-plan/well_profile/raw/master/well_profile/tests/trajectory1.xlsx')
        self.assertEqual(well.get_point(3245, depth_type='tvd')['pointType'], 'interpolated')
        self.assertEqual(well.get_point(3245.22, depth_type='tvd')['pointType'], 'survey')
        with self.assertRaises(ValueError):     # raising error for deeper TVD than deepest trajectory TVD
            well.get_point(3246, depth_type='tvd')


def run_assertions(obj, well, mdt):
    traj = well.trajectory
    obj.assertIsInstance(well.npoints, int, msg='points is not an integer')
    obj.assertEqual(traj[-1]['md'], mdt, msg='Target depth not reached')
    obj.assertEqual(traj[0]['md'], traj[0]['tvd'], msg='MD and TVD are different at first cell')
    obj.assertIn('pointType', traj[0], msg='pointType property was not found for first trajectory point')
