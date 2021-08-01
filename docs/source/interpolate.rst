|bgd|

.. |bgd| image:: https://github.com/pro-well-plan/opensource_apps/raw/master/resources/pwp-bgd.gif


Interpolating points along the trajectory
=========================================

You can get all the relevant data for any specifc MD value along the wellbore trajectory.

.. code-block:: python

    >>> import well_profile as wp
    >>> well = wp.load('trajectory1.xlsx')   # loading excel file
    >>> wb1.get_point(3750)     # get data at 3750m MD

.. code-block:: python

    {'md': 3750,
     'dl': 0.5573264781490191,
     'inc': 52.9126735218509,
     'azi': 22.04,
     'north': 113.70285532280701,
     'east': 1340.3801459482888,
     'tvd': 3220.9879889843924,
     'pointType': 'interpolated',
     'sectionType': 'drop-off'}

|load_excel|

.. |load_excel| image:: /figures/load_excel.png
                    :scale: 35%