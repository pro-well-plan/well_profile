Changing the azimuth
====================

.. code-block:: python

    >>> import well_profile as wp
    >>> well_1 = wp.load('trajectory1.xlsx', change_azimuth=180)      # LOAD WELL 1 --> Azimuth: + 180°
    >>> well_2 = wp.get(6000, profile='J', kop=2000, eob=4000, build_angle=85,
    >>>                 set_start={'east':2000}, change_azimuth=42)       # GET WELL 2 --> Azimuth: + 42°
    >>> well_3 = wp.load('trajectory2.xlsx', set_start={'north':-4000})        # LOAD WELL 3
    >>> well_1.plot(add_well=[well_2, well_3],
    >>>             names=['first well name',
    >>>                    'second well name',
    >>>                    'third well name']).show()        # Generate 3D plot for well 1 including wells 2 and 3

|change_azi|

.. |change_azi| image:: /figures/change_azi.png
                    :scale: 30%