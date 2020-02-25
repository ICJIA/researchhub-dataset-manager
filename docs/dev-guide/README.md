# Overview

This guide is meant for Research Hub Dataset Manager's maintainer as well as those interested in the inner workings of the Dataset Manager.

## Contents

You will find in this guide:

- Overview: Current page.
- [App](app/): How the Python app is structured.
  - [`__main__.py`](app/main.md)
  - [Packages](app/util.md)
- [Database](database/): What the database contains.
  - [Database tables](database/tables.md)
- [Documentation](doc.md): This documentation site.
- [Miscellaneous](misc.md): Miscellaneous files and scripts.

## File structure

```
/
├─ app/
├─ database/
├─ datasets/
├─ docs/
├─ input/
├─ misc/
├─ temp/
...
├─ setup.ps1
└─ start.ps1
```

`/` on the top signifies the project root directory, which currently is `\\MAINFILESRV\r&a\DATA\researchhub-dataset-manager` or `P:\DATA\researchhub-dataset-manager`.

### Subdirectories

Each subdirectory in this project represents a specific feature of the Dataset Manager and may contain files and scripts to implement that.

- `/app/` contains Python scripts making up the Dataset Manager. See [the "App" pages](app/) for details.
- `/database/` contains a SQLite database file for the Dataset Manager, `database.db`. See [the "Database" pages](database/) for details.
- `/datasets/` contains all generated dataset outputs. See [the "Data Output" page](/guide/output.md) for details.
- `/doc/` contains files for building this documentation site. See [the "Documentation" page](documentation.md) for details.
- `/input/` is for user input files, which must be placed here before running the Dataset Manager to mannually updating the database. See [the "Update data" page](/guide/tasks/1-data.md) in the Guide for details on the input data format and more.
- `/misc/` contains files and scripts for miscellaneous jobs. See [the "Miscellaneous" page](misc.md) for details.
- `/temp/` is for temporary outputs that are automatically generated during the process of carryoug out tasks are placed here. The directory should remain empty as all temporary outputs are automatically removed once the task is complete whether successfully or not.

### Scripts

This project contains the following PowerShell scripts for the end users.

- `/setup.ps1` is a PowerShell script to set up the Python virtual environment for the Data Manager application.
- `/start.ps1` is a PowerShell script to spin up the Data Manager application.