# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.8.0]

### Changed
- Org primary key is to be pipeline generated

### Added
- Org name and acronym together must be unique

### Removed
- Org versioning

## [0.7.0]

### Added
- Missing constraints
- Tests on the constraints
- `hapi_updated_date` and `hapi_replaced_date` fields

### Changed

- Small changes to other dates for HAPI v2

## [0.6.2]

### Changed

- Update requirements

## [0.6.1]

### Changed

- National risk location link

## [0.6.0]

### Added

- National risk tables and views

## [0.5.0]

### Added

- Humanitarian needs tables and views

## [0.4.0]

### Added

- Food security-related tables and views

## [0.3.2]

### Changed

- HDX provider code and name change

## [0.3.1]

### Changed

- Renamed resource column `filename` to `name`

## [0.3.0]

### Added

- Tests for creating and populating tables and views

## [0.2.0]

### Changed

- Dependency on hdx-python-database is optional
- View definitions converted to parameter dicts

## [0.1.1]

### Fixed

- Compatability with `views` module moved to `hdx-python-database`
- Removed `timezone` extra which was not properly configured

## [0.1.0]

### Added

- Hatch configuration files
- Contribute
- Pre commit hooks
- View module
- Views for all tables

### Changed

- Renamed `orgtype` module to `org_type`

### Removed

- Removed committed package info (.egg-info)

## [0.0.4]

### Added

- Copied relevant files from HAPI pipelines
- Adapted file references to work as a stand-alone package
- Setup.py for building as a package
