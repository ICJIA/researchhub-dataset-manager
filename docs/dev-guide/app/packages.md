# Packages

The Python application consists of give custom utility packages to support the tasks carried out by Research Hub Dataset Manager. Each utility package implements a specific aspect of the Dataset Manager's functionality as described below.

These packages share a common structure, where `__init__.py` exposes package objects to be publicly accessible, mostly defined in `main.py`, and `misc.py` defines miscellaneous helper functions specific to the given package.

::: warning NOTE
This page only provides a high-level description of the modules and scripts. To investigate the code in detail, go to [the project's GitHub repository](https://github.com/icjia/researchhub-dataset-manager) or clone the repository to your local workstation.
:::

## `data`

Package `data` contains modules for preparing data from various sources so that they can be used to update the database.

::: tip TIP
See [the "Data Sources" page](/dev-guide/sources.md) to read more on each data source and how the sources relate to the dataset outputs.
:::

* `data.bridgepop` defines functions to fetch the Bridged Race Population Estimates data from its online source and reshape the data into a proper format for updating the "BridgePop" table in the database.
* `data.chri` defines functions to query Criminal History Records Information data in the local SQL database and reshape the query result into a proper format for updating the "Data" table in the database.
* `data.idjj` defines functions to query Illinois Department of Juvenile Justice data in the local SQL database and reshape the query result into a proper format for updating the "Data" table in the database.
* `data.idoc` defines functions to query Illinois Department of Corrections data in the local SQL database and prepare the query result for updating the "Data" table in the database.
* `data.jail` defines functions to read the Jail and Detention Standards
data from its network drive location and reshape the data into a proper format for updating the "Data" table in the database.
* `data.laus` defines functions to fetch the Local Area Unemployment Statistics (LAUS) estimates data from its online source and reshape the data into a proper format for updating the "Data" table in the database.
* `data.sapie` defines functions to fetch the Small Area Income and Poverty Estimates (SAIPE) data from its online source and reshape the data into a proper format for updating the "Data" table in the database.
* `data.ucr` defines functions to fetch the annual Uniform Crime Reports data from its online source and reshape the data into a proper format for updating the "Data" table in the database.

## `database`

Package `database` contains modules for interacting with the database file, `/database/database.db`.

* `database.conn` defines the `Conn` class with a set of methods to facilitate establishing the database connection and use it to send queries and receive query results.
* `database.dbread` defines functions to read from the database tables.
* `database.dbwrite` defines functions to write to the database tables.
* `database.main` defines functions to create/drop temporary tables and update existing tables in the database.

## `dataset`

Package `dataset` contains modules for generating data and metadata files.

* `dataset.generate_data` defines functions supporting generating the data file for the given dataset.
* `dataset.generate_metadata` defines functions supporting generating the metadata file for the given dataset.
* `dataset.main` defines functions for generating data outputs.

## `fs`

Package `fs` contains modules for interacting with the filesystem and read or write files from or to the disk.

* `fs.fread` defines functions supporting reading files from the disk.
* `fs.fwrite` defines functions supporting writing files to the disk as well as deleting existing files.
* `fs.main` defines functions for interacting with the file system to carry out the Dataset Manager's tasks.

## `ui`

Package `ui` contains modules for defining the user interface of the Dataset Manager's command-line application.

* `ui.io` defines functions for high-level input/output operations involving the database or file system.
* `ui.main` defines functions for high-level user interface operations to handle user inputs and carry out specified tasks.
* `ui.prompt` defines functions to prompt for user input at the various stages of using the Dataset Manager.
