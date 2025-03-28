# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.9.11

### Changed

- Lat and lon from WFP market nullable for market "National Average"

## 0.9.11

### Changed

- Added Rainfall table and views

## 0.9.10

### Fixed

- Align VAT definitions with database tables

## 0.9.9

### Changed

- Added admin level to WFP Market table
- Allow intensity of deprivation in poverty rate to be nullable
- Allow non-appeal funding in funding table

## 0.9.8

### Fixed

- Re-release previous changes

## 0.9.7

### Changed

- Changed endpoint names for conflict event, food price, food security, population, poverty rate, and refugees tables
- Include origin and asylum in data availability for refugees and returnees

## 0.9.6

### Fixed

- Fixed data_availability_vat primary key and indices
- Added indices for each new admin_level column in other tables

## 0.9.5

### Changed

- Changed precision of poverty rate constraint

## 0.9.4

### Added

- Admin_level to views

## 0.9.3

### Fixed

- Inconsistent definitions of reference_period_start, reference_period_end

## 0.9.2

### Changed

- Freeform category for HNO instead of gender, age, disabled, population group

## 0.9.1

### Added

- Return views from prepare_hapi_views call

## 0.9.0

### Added

- major refactoring to allow partial/incremental standardisation of
  subnational geocodes.  Added `provider_admin1_name` and
  `provider_admin2_name` to the primary keys of subcategory tables
  (except `food_price`), as appropriate.
- added `provider_admin1_name` and `provider_admin2_name` to `idps`,
  `humanitarian_needs`, `operational_presence`, `conflict_event`,
  `food_security`, `population`, and `wfp_market` (and associated views,
  VATS, and tests)
- renamed existing column `admin1_name` to `provider_admin1_name` in
  `povert\_rate` for consistency (and updated tests and VAT)
- updated `food_price_view` and VAT to include `provider_admin1_name` and `provider_admin2_name` from `wfp_market`
- updated `poverty_rate_view` and VAT to include `admin1_name` from `admin1` table
- made `reference_period_start` part of the primary key for `population_vat` (originally omitted in error)

### Changed

- added "Producer" to the `PriceType` enum
- humanitarian needs table changes - replace gender, age, disability and
  population group columns with freeform category column

## 0.8.17

### Added

- `operation` and additional primary keys to `idps` table

## 0.8.16

### Added

- `idps` table, view, and VAT
- `returnees` table, view, and VAT
- `data_availability` VAT
- new constraint: `greater\_than\_constraint`

### Changed

- corrected `availability\_view` to `data\_availability\_view`

## 0.8.15

### Added

- `data\_availability\_view`, which shows the locations available for each API endpoint

### Changed

- Added idps table and view (including materialised view)
- Applied feedback from this
  [SQLAlchemy discussion](sqlalchemy/sqlalchemy#11748)
  to allow usage of type annotations defined in Base classes

## 0.8.14

### Fixed

- Rename `has\_hno` to `has\_hrp` and add new fields to food prices table

## 0.8.13

### Changed

- Added `has\_hrp` and `in\_gho` fields to `location` table and view

### Fixed

- Rename fields in VAT tables


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
