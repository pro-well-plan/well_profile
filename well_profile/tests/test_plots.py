from unittest import TestCase
from well_profile import load


class TestPlots(TestCase):

    def test_dark_mode(self):
        well = load(r'https://github.com/pro-well-plan/well_profile/raw/master/well_profile/tests/trajectory1.xlsx')
        fig = well.plot(style={'darkMode': True})
        self.assertEqual(fig.layout.template.layout.mapbox.style, 'dark')

    def test_color(self):
        well = load(r'https://github.com/pro-well-plan/well_profile/raw/master/well_profile/tests/trajectory1.xlsx')
        well.plot(style={'color': 'dls'})

    def test_size(self):
        well = load(r'https://github.com/pro-well-plan/well_profile/raw/master/well_profile/tests/trajectory1.xlsx')
        well.plot(style={'size': 5})

    def test_top_view(self):
        well = load(r'https://github.com/pro-well-plan/well_profile/raw/master/well_profile/tests/trajectory1.xlsx')
        fig = well.plot(plot_type='top', style={'darkMode': True})
        self.assertEqual(fig.layout.template.layout.mapbox.style, 'dark')
