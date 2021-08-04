|bgd|

.. |bgd| image:: https://github.com/pro-well-plan/opensource_apps/raw/master/resources/pwp-bgd.gif


Plotting Trajectories
=====================

3D view - single trajectory
---------------------------

.. code-block:: python

    >>> import well_profile as wp
    >>> w1 = wp.load('wellbore1.xlsx')
    >>> w1.plot().show()

|3d_single|

.. |3d_single| image:: /figures/3d_single.png
                    :scale: 50%

3D view - plot multiple trajectories
------------------------------------

Same location
_____________

.. code-block:: python

    >>> import well_profile as wp
    >>> well_1 = wp.load('trajectory1.xlsx')      # LOAD WELL 1
    >>> well_2 = wp.get(5000, profile='J', kop=2000, eob=3000, build_angle=85)       # GET WELL 2
    >>> well_3 = wp.load('trajectory2.xlsx')        # LOAD WELL 3
    >>> well_1.plot(add_well=[well_2, well_3],
    >>>             names=['first well name',
    >>>                    'second well name',
    >>>                    'third well name']).show()        # Generate 3D plot for well 1 including wells 2 and 3

|multiple_same_loc|

.. |multiple_same_loc| image:: /figures/multiple_same_loc.png
                    :scale: 35%


Different location
__________________

.. code-block:: python

    >>> import well_profile as wp
    >>> well_1 = wp.load('trajectory1.xlsx')      # LOAD WELL 1
    >>> well_2 = wp.get(5000, profile='J', kop=2000, eob=3000, build_angle=85, set_start={'east':2000})       # GET WELL 2 --> North: 0 m, East: 2000 m
    >>> well_3 = wp.load('trajectory2.xlsx', set_start={'north':-3000})        # LOAD WELL 3 --> North: -3000 m, East: 0 m
    >>> well_1.plot(add_well=[well_2, well_3],
    >>>             names=['first well name',
    >>>                    'second well name',
    >>>                    'third well name']).show()        # Generate 3D plot for well 1 including wells 2 and 3

|multiple_diff_loc|

.. |multiple_diff_loc| image:: /figures/multiple_diff_loc.png
                    :scale: 35%


Top view
--------

.. code-block:: python

    >>> import well_profile as wp
    >>> w1 = wp.load('wellbore1.xlsx')
    >>> w2 = wp.load('wellbore2.xlsx')
    >>> w3 = wp.load('wellbore3.xlsx')
    >>> w4 = wp.load('wellbore4.xlsx')
    >>> w5 = wp.load('wellbore5.xlsx')
    >>> w1.plot(add_well=[w2, w3, w4], plot_type='top').show()

|top_view|

.. |top_view| image:: /figures/top_view.png
                    :scale: 50%

Versus view
-----------

.. code-block:: python

    >>> import well_profile as wp
    >>> w1 = wp.load('wellbore1.xlsx')
    >>> w2 = wp.load('wellbore2.xlsx')
    >>> w3 = wp.load('wellbore3.xlsx')
    >>> w4 = wp.load('wellbore4.xlsx')
    >>> w5 = wp.load('wellbore5.xlsx')
    >>> w1.plot(add_well=[w2, w3, w4, w5], plot_type='vs', x_axis='md', y_axis='dls').show()

|versus_view|

.. |versus_view| image:: /figures/versus_view.png
                    :scale: 50%

Dark mode
---------

on 3D view
__________

.. code-block:: python

    >>> import well_profile as wp
    >>> w1 = wp.load('wellbore1.xlsx')
    >>> w2 = wp.load('wellbore2.xlsx')
    >>> w3 = wp.load('wellbore3.xlsx')
    >>> w4 = wp.load('wellbore4.xlsx')
    >>> w5 = wp.load('wellbore5.xlsx')
    >>> w1.plot(add_well=[w2, w3, w4, w5], style={'darkMode': True}).show()

|3d_dark|

.. |3d_dark| image:: /figures/3d_dark.png
                    :scale: 50%

on Top view
___________

.. code-block:: python

    >>> w1.plot(add_well=[w2, w3, w4, w5], plot_type='top', style={'darkMode': True}).show()

|top_dark|

.. |top_dark| image:: /figures/top_dark.png
                    :scale: 50%

on Versus view
______________

.. code-block:: python

    >>> w1.plot(add_well=[w2, w3, w4, w5], plot_type='vs', x_axis='md', y_axis='dls', style={'darkMode': True}).show()

|vs_dark|

.. |vs_dark| image:: /figures/vs_dark.png
                    :scale: 50%