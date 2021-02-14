|bgd|

.. |bgd| image:: https://github.com/pro-well-plan/opensource_apps/raw/master/resources/pwp-bgd.gif


Multiple wells in one plot
==========================

Same location
-------------

.. code-block:: python

    >>> import well_profile as wp
    >>> well_1 = wp.load('trajectory1.xlsx')      # LOAD WELL 1
    >>> well_2 = wp.get(6000, profile='J', kop=2000, eob=3000, build_angle=85)       # GET WELL 2
    >>> well_3 = wp.load('trajectory2.xlsx')        # LOAD WELL 3
    >>> well_1.plot(add_well=[well_2, well_3],
    >>>             names=['first well name',
    >>>                    'second well name',
    >>>                    'third well name']).show()        # Generate 3D plot for well 1 including wells 2 and 3

|multiple_same_loc|

.. |multiple_same_loc| image:: /figures/multiple_same_loc.png
                    :scale: 30%


Different location
------------------

.. code-block:: python

    >>> import well_profile as wp
    >>> well_1 = wp.load('trajectory1.xlsx')      # LOAD WELL 1
    >>> well_2 = wp.get(6000, profile='J', kop=2000, eob=3000, build_angle=85, set_start={'east':2000})       # GET WELL 2 --> North: 0 m, East: 2000 m
    >>> well_3 = wp.load('trajectory2.xlsx', set_start={'north':-3000})        # LOAD WELL 3 --> North: -3000 m, East: 0 m
    >>> well_1.plot(add_well=[well_2, well_3],
    >>>             names=['first well name',
    >>>                    'second well name',
    >>>                    'third well name']).show()        # Generate 3D plot for well 1 including wells 2 and 3

|multiple_diff_loc|

.. |multiple_diff_loc| image:: /figures/multiple_diff_loc.png
                    :scale: 30%
