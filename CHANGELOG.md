# Changelog

## 2.1.0 (2023-05-10)

#### New Features

* Add `pause` and `unpause` methods to `Timer`.
#### Performance improvements

* start() and stop() check whether the timer is running or not before performing their actions
#### Docs

* update and reformat docstrings
#### Others

* change minimum python version to 3.10


## v2.0.0 (2023-04-15)

#### New Features

* add history property
* make Self typing python 3.10 compatible
#### Fixes

* initialize result in time_it
* update time_it to call average time correctly
#### Refactorings

* convert most members to properties
* revert datetime library usage back to time library
* import Self from typing_extensions
#### Others

* build v2.0.0
* update changelog
* update readme
* remove unused import
* remove current_elapsed_time() making package compatible with python >=3.6


## v1.3.0 (2023-03-31)

#### Fixes

* return <1{unit} from format_time when an empty string is returned
#### Refactorings

* convert format_time() to a staticmethod
* remove _get_time_unit and use divmod instead
#### Others

* build v1.3.0
* update changelog


## v1.2.0 (2023-03-30)

#### New Features

* add time_it decorator
* add 'elapsed' and 'elapsed_str' properties to Timer
* add subsecond_resolution to Timer constructor
#### Refactorings

* change start() test to chain start() to Timer()
* start() returns self so it can be chained to object creation
* decrease sleep time in time_it test function
* improve time_it() print message with name of function
* calculate 'elapsed' property from 'stop_time' if timer stopped instead of current time
#### Others

* build v1.2.0
* update changelog
* add time_it to import in __init__.py
* add warning to current_elapsed_time()
* add tests for 'elapsed' and 'elapsed_str' properties
* add time_it() test
* add timer.stop() and assert timer.elapsed


## v1.1.1 (2023-03-22)

#### Others

* build v1.1.1


## v1.1.0 (2023-03-13)

#### New Features

* add subsecond_resolution flag to current_elapsed_time()
#### Others

* build v1.1.0
* update changelog