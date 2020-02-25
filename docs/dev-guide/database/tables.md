# Database Tables

Research Hub Dataset Manager relies on data stored in the /database/database.db file, which contains a number of tables listed below.

::: warning NOTE
The Tool's database structure is drawn from the one used in the previous datasets maintenance practice. Accoringly, there are tables or columns that appear somewhat redundant or unused. This may change in future.  
:::

## BridgePop

The "BridgePop" table contains records drawn from [U.S. Census Populations With Bridged Race Categories](https://www.cdc.gov/nchs/nvss/bridged_race.htm) by the National Vial Statistics System. The records are in a disaggregated format--by year, county, bridged race group and gender, ethnicity (hispanic or not), and age--as in the original format. Records in this table are used for obtaining the population base for calculating the relevant rates in the dataset outputs.

The "BridgePop" table has the following columns:

- `year` (INTEGER): Year of each record.
- `fk_population_county` (INTEGER): A foreign key to the "County" table.
- `age` (INTEGER): .
- `race_gender` (INTEGER): .
- `hispanic` (INTEGER): .
- `value` (INTEGER): Data value.

## BridgePopOld

The "BridgePopOld" table contains aggregated records drawn from [U.S. Census Populations With Bridged Race Categories](https://www.cdc.gov/nchs/nvss/bridged_race.htm) by the National Vial Statistics System--in an old. The table is no longer maintained beyond the 2016 population estimates.

The "BridgePopOld" table has the following columns:

- `fk_bridgepop_county` (INTEGER): A foreign key to the "County" table.
- `year` (INTEGER): Year of each record.
- `fk_bridgepop_typepop` (INTEGER): A foreign key to the "TypePop" table.
- `value` (INTEGER): Data value.

## County

The "County" table contains information on Illinois counties and their characteristics.

The "County" table has the following columns:

- `id` (INTEGER): Unique identifier for each county.
- `fips_number` (REAL): The Federal Information Process Standard (FIPS) number for each county.
- `county_name` (TEXT): County name.
- `judicial_circuit` (TEXT): The Illinois circuit court under whose jurisdiction each county falls.
- `fk_county_typeunit` (REAL): A foreign key to the "TypeUnit" table.
- `alphabetical_oder` (REAL): The number of each county in alphebetical order.
- `region` (TEXT): Region of the county: Northern minus Cook, Northern - Cook, Central, or Southern
- `community_type` (TEXT): Categorization based on the proportion of rural area in a county: 1) "Completely Rural" means 100% rural, 2) "Mostly rural" means >50% rural, 3) "Mostly urban" means <50% rural, and 4) "Completely urban" means 0% rural
- `percent_rural` (REAL): Percentage of rural area in a county

## CountyCombined

The "CombinedCounty" table contains information regarding cases in which data for multiple counties are reported by a single county or a separate body of organization.

The "CountyCombined" table has the following columns:

- `id` (INTEGER): Unique indentifier for combined county records.
- `fk_combinedcounty_indicator` (INTEGER): A foreign key to the "Indicator" table.
- `year` (INTEGER): Year when the given combined county record is applicable.
- `fk_container_county` (INTEGER): A foreign key to the "County" table for the reporting county.
- `fk_contained_county` (INTEGER): A foreign key to the "County" table for the county reporting its data via another county.

## Data

The "Data" table is a storage for all the actual values from data sources except for the population estimates.

The "Data" table has the following columns:

- `fk_data_variable` (INTEGER): A foreign key to the "Variable" table.
- `fk_data_county` (INTEGER): A foreign key to the "County" table.
- `year` (INTEGER): Year of each record.
- `value` (REAL): Data value.

## Dataset

The "Dataset" table contains information about each dataset output, including the information that will be saved as its metadata file.

The "Dataset" table has the following columns:

- `id` (INTEGER): Unique identifier for each output table.
- `source_group` (INTEGER): Source group of each output table: 1 is AOIC, 2 is CHRI, 3 is IDOC, 4 is IDJJ, 5 is ISP, and 6 is others.
- `name` (TEXT): Name of each output table (as in the resulting `.csv` file).
- `old_name` (TEXT): Name of each output table as in the previous dataset maintenance system.
- `standard` (INTEGER): 1 if the table is in the standard format, 0 otherwise.
- `active` (INTEGER): 1 if the table is actively maintained, 0 otherwise.
- `fk_output_package` (INTEGER): A foreign key to the "Package" table.
- `name_full` (TEXT): Full name of each output table; included in the metadata.
- `source` (TEXT): Output data source.
- `year_type` (TEXT): Type of year: Calandar or Fiscal; included in the metadata.
- `year_min` (REAL): Minimum year value (for the earliest records); included in the metadata.
- `year_max` (REAL): Maximum year value (for the latest records); included in the metadata.
- `description` (TEXT): Description of each output; included in the metadata.
- `notes` (TEXT): Notes for each output; included in the metadata file.
- `column_name` (TEXT): A list of column names; included in the metadata.
- `column_info` (TEXT): A list of column descriptions; included in the metadata.

## TypeRate

The "TypeRate" table is a simple lookup table for bases to calculate rate.

The "TypeRate" table has the following columns:

- `id` (INTEGER): Unique identifier for each rate base.
- `description` (TEXT): Description of each rate base.

## TypePop

The "TypePop" table is a simple lookup table for age groups for aggregating population counts.

The "TypePop" table has the following columns:

- `id` (INTEGER): Unique indentifier for each age group.
- `description` (TEXT): Description of each age group.

## TypeUnit

The "TypeUnit" table is a simple lookup table for geographcal units.

The "TypeUnit" table has the following columns:

- `id` (INTEGER): Unique indentifier for each geography unit.
- `description` (TEXT): Description of each geography unit.

## Variable

The "Variable" table contains information about each "variable", whose records are collected by the ICJIA and incoporated into its published datasets.

Each variable is given a unique idenetifier. For instance, the indicator number of 10000 corresponds to "count" variable in the Orders of Protection table in the Administration Office of the Illinois Courts' Annual Report of the Illinois Courts.

::: warning NOTE
See [the "Data Sources" page](/dev-guide/sources.md) in the Guide for the link between variables and their sources.
:::

The "Variable" table has the following columns:

- `id` (INTEGER): Unique identifier for each variable.
- `name` (TEXT): Variable name
- `definition` (TEXT): Brief definition of each variable.
- `fk_variable_dataset` (INTEGER): A foreign key to the "Dataset" table.
- `fk_variable_typepop` (TEXT): A foreign key to the "TypePop" table.
- `fk_variable_typerate` (INTEGER): A foreign key to the "TypeRate" table.
