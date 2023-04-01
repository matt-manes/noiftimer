# Changelog

## 1.3.0 (2023-03-31)

#### Fixes

* return <1{unit} from format_time when an empty string is returned
#### Refactorings

* convert format_time() to a staticmethod
* remove _get_time_unit and use divmod instead


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