from unittest import TestCase
from well_profile import load


class TestStyle(TestCase):

    def test_dark_mode(self):
        well = load(r'https://github.com/pro-well-plan/well_profile/raw/master/well_profile/tests/trajectory1.xlsx')
        well.plot(style={'darkMode': True})

    def test_color(self):
        well = load(r'https://github.com/pro-well-plan/well_profile/raw/master/well_profile/tests/trajectory1.xlsx')
        well.plot(style={'color': 'dls'})

    def test_size(self):
        well = load(r'https://github.com/pro-well-plan/well_profile/raw/master/well_profile/tests/trajectory1.xlsx')
        well.plot(style={'size': 5})


def run_assertions(self, well, mdt):
    traj = well.trajectory
    self.assertIsInstance(well.points, int, msg='points is not an integer')
    self.assertEqual(traj[-1]['md'], mdt, msg='Target depth not reached')
    self.assertEqual(traj[0]['md'], traj[0]['tvd'], msg='MD and TVD are different at first cell')
    self.assertEqual(well.points, len(traj), msg='Number of points is not correct')
