# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.8.12

### Removed

- "POC" from `PopulationGroup` enum
- "POP" from `PopulationStatus` enum

## 0.8.11

### Fixed

- Missing location_ref in admin2 view

## 0.8.10

### Changed

- Adapted primary keys and make columsn nullable in the VAT tables
- Use the enum casting util in the patch table

## 0.8.9

### Fixed

- Some enums missing built from values

## 0.8.8

### Changed

- Rewrite enums to use values rather than variable names
- Switch from "*" to "all" for rollup in enums
- Add "intersectoral" to sample sector data (distinct from "all")
- Ensure that constraint names end consistently with "\_constraint"

## 0.8.7

### Changed

- Add unit to food\_price table primary key

## 0.8.6

### Changed

- Added food\_price view as tables by updating the toml parameter file
- Updated poverty\_rate view as table
- Updated operational\_presence view as table by updating the toml parameter file
- Made a few adhoc changes to the view as table generator code to accommodate Decimal columns

## 0.8.5

### Changed

- refactor DBPovertyRate to wide instead of narrow
- added org\_type\_description to operational\_presence\_view

## Removed

- rate\_constraint and `PovertyClassification` enum

## 0.8.4

### Added

- New constraints: rate\_constraint

### Changed

- refactor DBPovertyRate to track rates rather than population, and link to
  location (with admin1\_name as a text field)

## 0.8.3

### Changed

- fixed WFP commodity enum
- remove ALL ("*") from PovertyClassification enum
- change FLOAT to DECIMAL in funding, national\_risk, and food\_security

## 0.8.2

Miscellaneous fixes for pipelines

### Changed

- added from\_cods column to location, admin1, and admin2

## 0.8.1

Implemented the Food Prices subcategory.

### Added

- New tables and views: food\_price, wfp\_commodity, wfp\_market, currency
- New enums: PriceFlag, PriceType, CommodityCategory
- New constraints: non\_negative\_constraint, latlon\_constraint

## 0.8.0

### Changed

- Many small changes to align with V1 of the schema
- `resource` and `dataset` primary keys are now the UUID
- Use postgres instead of sqlite for testing
- Update GitHub Actions workflow to use postgres
- Created tables which reflect the views
- Programmatically obtain views

### Added

- New tables: humanitarian\_needs, funding, refugees, conflict\_event, poverty\_rate
- New enums: Gender, DisabledMarker, EventType, PopulationGroup, PopulationStatus, IPCPhase, PovertyClassification, IPCType, and RiskClass
- Generalized constraints

### Removed

- ipc\_phase, ipc\_type, age\_range, and gender tables

## [0.7.3]

### Fixed

- Incorrect constraint quotes in IPC type
- Clashing unique constraint names in admins

## [0.7.2]

### Added

- Patches table

## [0.7.1]

### Changed

- Removed constraint from food security

### Added
- Missing constraints
- Tests on the constraints
- `hapi_updated_date` and `hapi_replaced_date` fields

## [0.7.0]

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
