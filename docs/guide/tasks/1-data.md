# 1. Update data

The "Data" table holds most of the actual data records used to generate the packaged dataset outputs. In order to get an updated dataset, one must first update this table to have the latest numbers ready.

## Update automatically

Research Hub Dataset Manager offers an option to automatically update records drawn from a selection of data sources. Currently, automatic updating is available for the following data:

- Criminal History Records Information (CHRI)
  - Juvenile arrests (Microsoft SQL Server)
- Illinois Department of Corrections (IDOC)
  - Prison admissions (Microsoft SQL Server)
- Illinois Department of Juvenile Justice (IDJJ)
  - Juvenile court admissions and exits (Microsoft SQL Server).
- Illinois State Police (ISP)
  - Uniform Crime Report (online).
- Other sources
  - Illinois County Jail Population (Network drive P:/DATA/JAIL/).
  - Local Area Unemployment Statistics (Online).
  - Small Area Income and Poverty Estimates (Online).

## Update manually

Manually updating the "Data" table is available for all types of recrods. This requires a data input file in a specific format, i.e., that of the "SimpleCount" table, which looks like the following:

| fk_data_variable | year | fk_data_county | value |
| ---------------- | ---- | -------------- | ----- |
| 10000            | 2018 | 1              | 50    |
| 10000            | 2018 | 2              | 75    |
| ...              | ...  | ...            | ...   |

::: tip TIP
See [the "Database Tables" page](/dev-guide/database/tables.md) in the Developer Guide to learn more about the "Data" table and its columns. Also, see [the "Data Sources" section](/dev-guide/sources.md) in the Developer Guide to find which indicator code corresponds to which data.
:::

## Command-line Workflow

### Automatically update the "SimpleCount" table

1. Start the Dataset Manager on PowerShell

```powershell
p:/data/researchhub-dataset-manager/start

# alternatively:
# cd p:/data/researchhub-dataset-manager
# ./start
```

2. Choose: "- 1 - Update the 'Data' table in the database" (`1 + "Enter"`)
3. Choose: "- 1 - Automatically update database records from select data sources." (`1 + "Enter"`)
4. Choose the data source group for updating the table (`<input> + "Enter"`)
5. Specify the data source updating the database (`<input> + "Enter"`)
6. Review the temporary result generated in `/temp/`, i.e. `TempData.csv`
7. Confirm that the temporary result is as expected (`y + "Enter"`)
8. Restart the process (`y + "Enter"`), or quit the program (`n + "Enter"`)

### Manually update the "Data" table

1. Start the Dataset Manager on PowerShell

```powershell
p:/data/researchhub-dataset-manager/start
```

2. Choose: "- 1 - Update the 'Data' table in the database" (`1 + "Enter"`)
3. Choose: "- 2 - Manually provide input data for updating database records." (`2 + "Enter"`)
4. Place a correctly formated input file in `/input/`
5. Confirm that the input file is in the correct directory (`y + "Enter"`)
6. Confirm that the duplicates rows will be overwritten (`y + "Enter"`)
7. Review the temporary result generated in `/temp/`, i.e. `TempData.csv`
8. Confirm that the temporary result is as expected (`y + "Enter"`)
9. Restart the process (`y + "Enter"`), or quit the program (`n + "Enter"`)

## Tutorial

The following example illustrates the process of automatically updating the "Data" table with the latest prison admissions records from the MS SQL Server.

In this scenario, the program generates temporary outputs but the user decides _not_ to finish the task, exiting the program before updating the database.

![Example 1-1](/assets/img/guide_1_1.png)

![Example 1-2](/assets/img/guide_1_2.png)

![Example 1-3](/assets/img/guide_1_3.png)

![Example 1-4](/assets/img/guide_1_4.png)

![Example 1-5](/assets/img/guide_1_5.png)

![Example 1-6](/assets/img/guide_1_6.png)
