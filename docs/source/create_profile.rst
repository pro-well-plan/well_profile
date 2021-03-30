|bgd|

.. |bgd| image:: https://github.com/pro-well-plan/opensource_apps/raw/master/resources/pwp-bgd.gif


Creating a wellbore trajectory
==============================

.. autofunction:: well_profile.get

Vertical well
-------------

.. code-block:: python

    >>> import well_profile as wp
    >>> well = wp.get(3000,   # define target depth (md) in m or ft
    >>>               cells_no=100,   # (optional) define number of cells
    >>>               units='metric',   # (optional) define system of units 'metric' for meters or 'english' for feet
    >>>               set_start={'north': 0, 'east': 0, 'depth': 0})    # (optional) set the location of initial point
    >>> well.plot(names=['Wellbore ID']).show()

|create_vertical|

.. |create_vertical| image:: /figures/create_vertical.png
                    :scale: 30%


J-type well
-------------

.. code-block:: python

    >>> import well_profile as wp
    >>> well = wp.get(3000,   # define target depth (md) in m or ft
    >>>               profile='J',    # set J-type well profile
    >>>               kop=800,    # set kick off point in m or ft
    >>>               eob=2000,   # set end of build in m or ft
    >>>               build_angle=78,   # set build angle in °
    >>>               cells_no=100,   # (optional) define number of cells
    >>>               units='metric',   # (optional) define system of units 'metric' for meters or 'english' for feet
    >>>               set_start={'north': 0, 'east': 0, 'depth': 0})    # (optional) set the location of initial point
    >>> well.plot(names=['Wellbore ID']).show()

|create_j|

.. |create_j| image:: /figures/create_j.png
                    :scale: 30%


S-type well
-------------

.. code-block:: python

    >>> import well_profile as wp
    >>> well = wp.get(3000,   # define target depth (md) in m or ft
    >>>               profile='S',    # set S-type well profile
    >>>               kop=800,    # set kick off point in m or ft
    >>>               eob=1500,   # set end of build in m or ft
    >>>               build_angle=45,   # set build angle in °
    >>>               sod=1800,   # set start of drop in m or ft
    >>>               eod=2800,   # set end of drop in m or ft
    >>>               cells_no=100,   # (optional) define number of cells
    >>>               units='metric',   # (optional) define system of units 'metric' for meters or 'english' for feet
    >>>               set_start={'north': 0, 'east': 0, 'depth': 0})    # (optional) set the location of initial point
    >>> well.plot(names=['Wellbore ID']).show()

|create_s|

.. |create_s| image:: /figures/create_s.png
                    :scale: 30%


Horizontal single curve well
----------------------------

.. code-block:: python

    >>> import well_profile as wp
    >>> well = wp.get(3000,   # define target depth (md) in m or ft
    >>>               profile='H1',    # set horizontal single curve well profile
    >>>               kop=800,    # set kick off point in m or ft
    >>>               eob=1500,   # set end of build in m or ft
    >>>               build_angle=45,   # set build angle in °
    >>>               cells_no=100,   # (optional) define number of cells
    >>>               units='metric',   # (optional) define system of units 'metric' for meters or 'english' for feet
    >>>               set_start={'north': 0, 'east': 0, 'depth': 0})    # (optional) set the location of initial point
    >>> well.plot(names=['Wellbore ID']).show()

|create_h1|

.. |create_h1| image:: /figures/create_h1.png
                    :scale: 30%


Horizontal double curve well
----------------------------

.. code-block:: python

    >>> import well_profile as wp
    >>> well = wp.get(3000,   # define target depth (md) in m or ft
    >>>               profile='H2',    # set horizontal double curve well profile
    >>>               kop=800,    # set kick off point in m or ft
    >>>               eob=1500,   # set end of build in m or ft
    >>>               build_angle=45,   # set build angle in °
    >>>               cells_no=100,   # (optional) define number of cells
    >>>               units='metric',   # (optional) define system of units 'metric' for meters or 'english' for feet
    >>>               set_start={'north': 0, 'east': 0, 'depth': 0})    # (optional) set the location of initial point
    >>> well.plot(names=['Wellbore ID']).show()

|create_h2|

.. |create_h2| image:: /figures/create_h2.png
                    :scale: 30%


Using two points
----------------

This function allows to generate a wellbore trajectory by seeting kick-off point (KOP) and target.

.. autofunction:: well_profile.two_points

.. code-block:: python

    >>> import well_profile as wp
    >>> well = wp.two_points({'kickoff': {'north': 0, 'east': 0, 'tvd': 100},
    >>>                       'target': {'north': 500, 'east': 800, 'tvd': 800}})