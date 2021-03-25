[![Cover](https://github.com/pro-well-plan/opensource_apps/raw/master/resources/pwp-bgd.gif)](https://prowellplan.com)

[![Open Source Love svg2](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://github.com/pro-well-plan/well_profile/blob/master/LICENSE.md)
[![PyPI version](https://badge.fury.io/py/well-profile.svg)](https://badge.fury.io/py/well-profile)
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL_v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Webapp](https://img.shields.io/badge/WebApp-On-green.svg)](https://share.streamlit.io/jcamiloangarita/opensource_apps/app.py)
[![Documentation Status](https://readthedocs.org/projects/well_profile/badge/?version=latest)](http://well_profile.readthedocs.io/?badge=latest)
[![Build Status](https://www.travis-ci.org/pro-well-plan/well_profile.svg?branch=master)](https://www.travis-ci.org/pro-well-plan/well_profile)
[![Downloads](https://pepy.tech/badge/well-profile)](https://pepy.tech/project/well-profile)


## Introduction
well_profile is a tool to generate or load well profiles in 3D. Features are added as they
are needed; suggestions and contributions of all kinds are very welcome.

## Documentation

See here for the [complete well_profile package documentation](https://well_profile.readthedocs.io/en/latest/).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Get well_profile

* Users: Wheels for Python from [PyPI](https://pypi.python.org/pypi/well-profile/) 
    * `pip install well_profile`
* Developers: Source code from [Github](https://github.com/pro-well-plan/well_profile)
    * `git clone https://github.com/pro-well-plan/well_profile`
 
### Quick examples

Color by specified parameter: `e.g. 'dls'|'dl'|'tvd'|'md'|'inc'|'azi'`
```
import well_profile as wp
well = wp.load('trajectory1.xlsx')     # LOAD WELL
well.plot(style={'color': 'dls', 'size': 5}).show()
```
[![](https://user-images.githubusercontent.com/52009346/108047411-0e028580-7046-11eb-9de9-84c1cda2c903.png)](https://well-profile.readthedocs.io/en/latest/)

Also with dark mode:
```
well.plot(style={'darkMode': True, 'color': 'dls', 'size': 5}).show()
```
[![](https://user-images.githubusercontent.com/52009346/108048173-fed00780-7046-11eb-89f8-2a3b437b3047.png)](https://well-profile.readthedocs.io/en/latest/)

Plotting 3 wellbores:
* `Well 1 -> excel file: trajectory1.xlsx`
* `Well 2 -> generated well`
* `Well 3 -> excel file: trajectory2.xlsx`
```
import well_profile as wp
well_1 = wp.load('trajectory1.xlsx')      # LOAD WELL 1
well_2 = wp.get(6000, profile='J', kop=2000, eob=3000, build_angle=85, set_start={'east':2000})       # GET WELL 2 --> North: 0 m, East: 2000 m
well_3 = wp.load('trajectory2.xlsx', set_start={'north':-3000})        # LOAD WELL 3 --> North: -3000 m, East: 0 m
well_1.plot(add_well=[well_2, well_3],
            names=['first well name',
                   'second well name',
                   'third well name']).show()        # Generate 3D plot for well 1 including wells 2 and 3
```
<a href="https://youtu.be/X7Bs9_7NdRM">
   <img alt="Qries" src="https://well-profile.readthedocs.io/en/latest/_images/multiple_diff_loc.png"
   width=700" height="400">
</a>        

## Contributing

Please read [CONTRIBUTING](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## History ##
This tool was initially written and is maintained by [Pro Well Plan
AS](http://www.prowellplan.com/) as a free, simple, easy-to-use way to perform
torque and drag calculations along the well that can be tailored to our needs, and as contribution to the
free software community.

## License

This project is licensed under the GNU Lesser General Public License v3.0 - see the [LICENSE](LICENSE.md) file for details


*for further information contact juan@prowellplan.com*

[![](https://user-images.githubusercontent.com/52009346/69100304-2eb3e800-0a5d-11ea-9a3a-8e502af2120b.png)](https://prowellplan.com)
