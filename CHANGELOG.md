# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).


## [v0.5.1] - 2021-02-15
### Added
- Function two_points to generate a trajectory by setting KOP and Target
- Method to add wellbore location
- Including plot style
- Well.info
### Changed
- Get trajectory as list of dicts
- Set equidistant as default
- ### Fixed
- Minor issues

## [v0.4.1] - 2021-01-15
### Added
- Allows input data as list of lists

## [v0.4.0] - 2020-11-25
### Added
- Vizualization: Dark mode
- Show DLS results
### Changed
- Range for DLS

## [v0.2.9] - 2020-10-14
### Added
- Possibility to keep original points when loading a wellpath
- New parameter to manipulate azimuth for the entire well
### Fixed
- Minor issues

## [v0.1.9] - 2020-09-29
### Added
- Set initial depth and coordinates for a new well

## [v0.0.9] - 2020-09-18
### Fixed
- Issue when values in excel spreedsheet are not set as numbers

## [v0.0.8.1] - 2020-09-08
### Changed
- TVD is not required to load data but still can be included
- Allowed to use different column names. e.g. md, MD, measured depth, etc
### Fixed
- Method to convert trajectory to a dataframe

## [v0.0.7] - 2020-09-07
### Added
- Dataframe is now allowed to load a wellpath
- Files in format .csv are allowed to load a wellpath
- Method to convert trajectory to a dataframe
- Units as attribute
### Changed
- Plot function returns a figure object
### Fixed
- Calcs for creating horizontal double curve

## [v0.0.6] - 2020-09-02
### Changed
- Generate 3D plots (north, east and depth)
### Added
- Add several wells into the same plot

## [v0.0.5] - 2020-09-01
### Added
- Load a wellpath using an excel file
