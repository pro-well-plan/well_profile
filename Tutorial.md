## Index ##

* [1. Create a new wellbore trajectory.](#1.-Create)
* [2. Load your own wellbore trajectory.](#2.-Load)

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
<img width="1026" alt="Screenshot 2020-10-05 at 12 44 25" src="https://user-images.githubusercontent.com/52009346/95070515-82c4cb00-0708-11eb-9e6d-51ea2e78eb3f.png">

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
<img width="1057" alt="Screenshot 2020-10-05 at 12 50 41" src="https://user-images.githubusercontent.com/52009346/95071063-61b0aa00-0709-11eb-8109-4604b9f1d2e6.png">

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
<img width="1009" alt="Screenshot 2020-10-05 at 12 56 03" src="https://user-images.githubusercontent.com/52009346/95071557-22368d80-070a-11eb-9a6b-3fc8c235b297.png">

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
<img width="1016" alt="Screenshot 2020-10-05 at 12 59 02" src="https://user-images.githubusercontent.com/52009346/95071818-8ce7c900-070a-11eb-845f-d38990aeab03.png">

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
<img width="1023" alt="Screenshot 2020-10-05 at 13 01 36" src="https://user-images.githubusercontent.com/52009346/95072056-e94ae880-070a-11eb-9c9b-7f071c8fea96.png">

## 2. Load
