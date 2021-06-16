from unittest import TestCase
from well_profile import get


class TestGetTrajectory(TestCase):

    def test_get(self):

        profile = ['V', 'J', 'S', 'H1', 'H2']

        for x in profile:
            well = get(100, points=100, profile=x, build_angle=45, kop=20, eob=40, sod=60, eod=80,
                       kop2=60, eob2=80)

            run_assertions(self, well, 100)


def run_assertions(obj, well, mdt):
    traj = well.trajectory
    obj.assertIsInstance(well.points, int, msg='points is not an integer')
    obj.assertEqual(traj[-1]['md'], mdt, msg='Target depth not reached')
    obj.assertEqual(traj[0]['md'], traj[0]['tvd'], msg='MD and TVD are different at first cell')
    obj.assertEqual(well.points, len(traj), msg='Number of points is not correct')
