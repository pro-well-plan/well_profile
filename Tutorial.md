## Index ##

* [Create a new wellbore trajectory.](https://github.com/pro-well-plan/well_profile/blob/master/Tutorial.md#1-create)
  * [1.1. Vertical well](https://github.com/pro-well-plan/well_profile/blob/master/Tutorial.md#11-vertical-well)
  * [1.2. J-type well](https://github.com/pro-well-plan/well_profile/blob/master/Tutorial.md#12-j-type-well)
  * [1.3. S-type well](https://github.com/pro-well-plan/well_profile/blob/master/Tutorial.md#13-s-type-well)
  * [1.4. Horizontal single curve well](https://github.com/pro-well-plan/well_profile/blob/master/Tutorial.md#14-horizontal-single-curve-well)
  * [1.5. Horizontal double curve well](https://github.com/pro-well-plan/well_profile/blob/master/Tutorial.md#15-horizontal-double-curve-well)
* [Load your own wellbore trajectory.](https://github.com/pro-well-plan/well_profile/blob/master/Tutorial.md#2-load)
  * [2.1. From excel file](https://github.com/pro-well-plan/well_profile/blob/master/Tutorial.md#21-from-excel-file)
  * [2.2. From csv file](https://github.com/pro-well-plan/well_profile/blob/master/Tutorial.md#22-from-csv-file)
* [Plot two or more wells.](https://github.com/pro-well-plan/well_profile/blob/master/Tutorial.md#3-two-or-more-wells-in-one-plot)
* [Set initial location.](https://github.com/pro-well-plan/well_profile/blob/master/Tutorial.md#4-set-initial-location)
* [Change well direction (azimuth).](https://github.com/pro-well-plan/well_profile/blob/master/Tutorial.md#5-change-azimuth)


## 1. Create

### 1.1. Vertical well
```
>>> import well_profile as wp 
>>> well = wp.get(3000,   # define target depth (md) in m or ft
              cells_no=100,   # (optional) define number of cells
              units='metric',   # (optional) define system of units 'metric' for meters or 'english' for feet
              set_start={'north': 0, 'east': 0, 'depth': 0})    # (optional) set the location of initial point

>>> well.plot(names=['Wellbore ID']).show()
```
<img width="1026" src="https://user-images.githubusercontent.com/52009346/95070515-82c4cb00-0708-11eb-9e6d-51ea2e78eb3f.png">

### 1.2. J-type well
```
>>> import well_profile as wp 
>>> well = wp.get(3000,   # define target depth (md) in m or ft
              profile='J',    # set J-type well profile 
              kop=800,    # set kick off point in m or ft
              eob=2000,   # set end of build in m or ft
              build_angle=78,   # set build angle in °
              cells_no=100,   # (optional) define number of cells
              units='metric',   # (optional) define system of units 'metric' for meters or 'english' for feet
              set_start={'north': 0, 'east': 0, 'depth': 0})    # (optional) set the location of initial point

>>> well.plot(names=['Wellbore ID']).show()
```
<img width="1057" src="https://user-images.githubusercontent.com/52009346/95071063-61b0aa00-0709-11eb-8109-4604b9f1d2e6.png">

### 1.3. S-type well
```
>>> import well_profile as wp 
>>> well = wp.get(3000,   # define target depth (md) in m or ft
              profile='S',    # set S-type well profile 
              kop=800,    # set kick off point in m or ft
              eob=1500,   # set end of build in m or ft
              build_angle=45,   # set build angle in °
              sod=1800,   # set start of drop in m or ft
              eod=2800,   # set end of drop in m or ft
              cells_no=100,   # (optional) define number of cells
              units='metric',   # (optional) define system of units 'metric' for meters or 'english' for feet
              set_start={'north': 0, 'east': 0, 'depth': 0})    # (optional) set the location of initial point

>>> well.plot(names=['Wellbore ID']).show()
```
<img width="1009" src="https://user-images.githubusercontent.com/52009346/95071557-22368d80-070a-11eb-9a6b-3fc8c235b297.png">

### 1.4. Horizontal single curve well
```
>>> import well_profile as wp 
>>> well = wp.get(3000,   # define target depth (md) in m or ft
              profile='H1',    # set horizontal single curve well profile 
              kop=800,    # set kick off point in m or ft
              eob=1500,   # set end of build in m or ft
              build_angle=45,   # set build angle in °
              cells_no=100,   # (optional) define number of cells
              units='metric',   # (optional) define system of units 'metric' for meters or 'english' for feet
              set_start={'north': 0, 'east': 0, 'depth': 0})    # (optional) set the location of initial point

>>> well.plot(names=['Wellbore ID']).show()
```
<img width="1016" src="https://user-images.githubusercontent.com/52009346/95071818-8ce7c900-070a-11eb-845f-d38990aeab03.png">

### 1.5. Horizontal double curve well
```
>>> import well_profile as wp 
>>> well = wp.get(3000,   # define target depth (md) in m or ft
              profile='H2',    # set horizontal double curve well profile 
              kop=800,    # set kick off point in m or ft
              eob=1500,   # set end of build in m or ft
              build_angle=45,   # set build angle in °
              cells_no=100,   # (optional) define number of cells
              units='metric',   # (optional) define system of units 'metric' for meters or 'english' for feet
              set_start={'north': 0, 'east': 0, 'depth': 0})    # (optional) set the location of initial point

>>> well.plot(names=['Wellbore ID']).show()
```
<img width="1023" src="https://user-images.githubusercontent.com/52009346/95072056-e94ae880-070a-11eb-9c9b-7f071c8fea96.png">

## 2. Load

### 2.1. From excel file
Example of a file is shown below. In case TVD is not included, the package calculates the values using the minimum curvature method. North and East coordinates also can be included.

<img width="437" src="https://user-images.githubusercontent.com/52009346/95073678-8870df80-070d-11eb-9449-ad073520027c.png">

```
>>> import well_profile as wp 
>>> well = wp.load('trajectory1.xlsx',   # define target depth (md) in m or ft
                   cells_no=100,  # (optional) define number of cells
                   units='metric',  # (optional) define system of units 'metric' for meters or 'english' for feet
                   set_start={'north': 0, 'east': 0, 'depth': 0})  # (optional) set the location of initial point

>>> well.plot(names=['loaded from excel']).show()
```
<img width="1038" src="https://user-images.githubusercontent.com/52009346/95073443-2912cf80-070d-11eb-9ac2-9b03a5663fff.png">

### 2.2. From csv file
```
>>> import well_profile as wp 
>>> well = wp.load('trajectory1.csv',   # define target depth (md) in m or ft
                   cells_no=100,  # (optional) define number of cells
                   units='metric',  # (optional) define system of units 'metric' for meters or 'english' for feet
                   set_start={'north': 0, 'east': 0, 'depth': 0})  # (optional) set the location of initial point

>>> well.plot(names=['loaded from csv']).show()
```
<img width="1031" src="https://user-images.githubusercontent.com/52009346/95074838-7c861d00-070f-11eb-9b7e-218c81353181.png">

## 3. Two or more wells in one plot
```
>>> import well_profile as wp 
>>> well_1 = wp.load('trajectory1.xlsx')      # LOAD WELL 1
    well_2 = wp.get(6000, profile='J', kop=2000, eob=4000, build_angle=85)       # GET WELL 2
    well_3 = wp.load('trajectory2.xlsx')        # LOAD WELL 3

>>> well_1.plot(add_well=[well_2, well_3],
                names=['first well name',
                       'second well name',
                       'third well name']).show()        # Generate 3D plot for well 1 including wells 2 and 3
```
<img width="1109" src="https://user-images.githubusercontent.com/52009346/96148790-e6b97180-0f08-11eb-9bc0-01af1cd6c378.png">

## 4. Set initial location
Define the initial surface location for the respective well.
```
>>> import well_profile as wp 
>>> well_1 = wp.load('trajectory1.xlsx')      # LOAD WELL 1
    well_2 = wp.get(6000, profile='J', kop=2000, eob=4000, build_angle=85, set_start={'east':2000})       # GET WELL 2 --> North: 0 m, East: 2000 m
    well_3 = wp.load('trajectory2.xlsx', set_start={'north':-4000})        # LOAD WELL 3 --> North: -4000 m, East: 0 m

>>> well_1.plot(add_well=[well_2, well_3],
                names=['first well name',
                       'second well name',
                       'third well name']).show()        # Generate 3D plot for well 1 including wells 2 and 3
```
<img width="1063" src="https://user-images.githubusercontent.com/52009346/95081611-1357d700-071a-11eb-8679-b8a349d9d0d4.png">

## 5. Change azimuth
Modififying the direction of the entire trajectory.
```
>>> import well_profile as wp 
>>> well_1 = wp.load('trajectory1.xlsx', change_azimuth=180)      # LOAD WELL 1 --> Azimuth: + 180°
    well_2 = wp.get(6000, profile='J', kop=2000, eob=4000, build_angle=85, 
                    set_start={'east':2000}, change_azimuth=42)       # GET WELL 2 --> Azimuth: + 42°
    well_3 = wp.load('trajectory2.xlsx', set_start={'north':-4000})        # LOAD WELL 3

>>> well_1.plot(add_well=[well_2, well_3],
                names=['first well name',
                       'second well name',
                       'third well name']).show()        # Generate 3D plot for well 1 including wells 2 and 3
```
<img width="1059" src="https://user-images.githubusercontent.com/52009346/96149312-74955c80-0f09-11eb-8b28-21c2dcb36cc6.png">
