# Tasks Overview

::: warning NOTE
See [the previous "Getting Started" section](/guide/get-started.md) to see how to start the program.
:::

ICJIA Web Dataset Maintanence Tool allows you to carry out three key tasks required to keep the underlying database updated and generate datasets from the database. These task include:

1. Update the "Data" table in the database.
2. Update the "BridgePop" table in the database.
3. Generate packaged dataset outputs

The first and second tasks require appropriate data inputs and, once completed, change the corresponding tables in the database file, `/database/database.db`. The third task does not require data input but uses records in the database; once completed, new packaged dataset zipfile is stored in `/datasets/` subdirectory.

::: tip TIP
See [the "File structure" section](/dev-guide/#file-structure) in the Developer Guide for details on the file structure of the Dataset Manager directory.

See [the "Database" page](/dev-guide/database/) in the Developer Guide to learn more about the structure of the database that holds all the underlying records used to generate datasets.  
:::
