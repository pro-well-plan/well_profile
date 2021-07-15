|bgd|

.. |bgd| image:: https://github.com/pro-well-plan/opensource_apps/raw/master/resources/pwp-bgd.gif


Loading a wellbore trajectory
=============================

.. autofunction:: well_profile.load

From excel file
---------------
Example of a file is shown below. In case TVD is not included, the package calculates the values using the minimum
curvature method. North and East coordinates also can be included.

|excel_data|

.. |excel_data| image:: /figures/excel_data.png
                    :scale: 30%

.. code-block:: python

    >>> import well_profile as wp
    >>> well = wp.load('trajectory1.xlsx',   # define target depth (md) in m or ft
    >>>               set_info={'dlsResolution', 'wellType': 'onshore'|'offshore', 'units': 'metric'|'english'},
    >>>               # (optional) define the resolution for dls calculation, well type and system of units 'metric'
    >>>               # for meters or 'english' for feet
    >>>               set_start={'north': 0, 'east': 0, 'depth': 0})  # (optional) set the location of initial point
    >>> well.plot(names=['loaded from excel']).show()

|load_excel|

.. |load_excel| image:: /figures/load_excel.png
                    :scale: 30%

From csv file
-------------

.. code-block:: python

    >>> import well_profile as wp
    >>> well = wp.load('trajectory1.csv',   # define target depth (md) in m or ft
    >>>               set_info={'dlsResolution', 'wellType': 'onshore'|'offshore', 'units': 'metric'|'english'},
    >>>               # (optional) define the resolution for dls calculation, well type and system of units 'metric'
    >>>               # for meters or 'english' for feet
    >>>               set_start={'north': 0, 'east': 0, 'depth': 0})  # (optional) set the location of initial point
    >>> well.plot(names=['loaded from csv']).show()

|load_csv|

.. |load_csv| image:: /figures/load_csv.png
                    :scale: 30%