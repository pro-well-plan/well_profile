from unittest import TestCase
from well_profile import two_points


class TestTwoPoints(TestCase):

    def test_gen_two_points_case1(self):
        # change in vertical = change in horizontal
        point_1 = {'north': 50, 'east': 20, 'tvd': 300}
        point_2 = {'north': 0, 'east': -500, 'tvd': 800}

        well = two_points({'kickoff': point_1, 'target': point_2})

        two_points_assertions(self, well, point_1, point_2)
        run_assertions(self, well, well.trajectory[-1]['md'])

    def test_gen_two_points_case2(self):
        # change in vertical < change in horizontal
        point_1 = {'north': -35, 'east': 21, 'tvd': 300}
        point_2 = {'north': -100, 'east': 800, 'tvd': 800}

        well = two_points({'kickoff': point_1, 'target': point_2})

        two_points_assertions(self, well, point_1, point_2)
        run_assertions(self, well, well.trajectory[-1]['md'])

    def test_gen_two_points_case3(self):
        # change in vertical > change in horizontal
        point_1 = {'north': 100, 'east': -48, 'tvd': 300}
        point_2 = {'north': 500, 'east': 0, 'tvd': 1900}

        well = two_points({'kickoff': point_1, 'target': point_2})

        two_points_assertions(self, well, point_1, point_2)
        run_assertions(self, well, well.trajectory[-1]['md'])


def run_assertions(obj, well, mdt):
    traj = well.trajectory
    obj.assertIsInstance(well.points, int, msg='points is not an integer')
    obj.assertEqual(traj[-1]['md'], mdt, msg='Target depth not reached')
    obj.assertEqual(traj[0]['md'], traj[0]['tvd'], msg='MD and TVD are different at first cell')
    obj.assertEqual(well.points, len(traj), msg='Number of points is not correct')


def two_points_assertions(obj, well, point_1, point_2):
    obj.assertEqual(well.trajectory[-1]['north'], point_2['north'], msg='Getting wrong north at TD')
    obj.assertEqual(well.trajectory[-1]['east'], point_2['east'], msg='Getting wrong east at TD')
    obj.assertEqual(well.trajectory[0]['north'], point_1['north'], msg='Getting wrong north at Surface')
    obj.assertEqual(well.trajectory[0]['east'], point_1['east'], msg='Getting wrong east at Surface')