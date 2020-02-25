# 2. Update population

The "BridgePop" table keeps the actual county-level population estimates used to generate the packaged dataset outputs. This is what is used to calculate "rate" column values.

## Update automatically

Research Hub Dataset Manager can update "BridgePop" in a fully automated fashion. In fact, to minimize the chances of human errors, the current documentation strongly recommends using an automatic option for adding the latest population estimates to the database.

## Update manually

Although not recommended, the Dataset Manager also offers an option to mannually update the table. The process is largely identical to that of manually updating the "SimpleCount" data described above. The "BridgePop" table format is as follows:

| year | fk_bridgepop_county | age | race_gender | hispanic | value |
| ---- | ------------------- | --- | ----------- | -------- | ----- |
| 2018 | 1                   | 0   | 1           | 1        | 100   |
| 2018 | 1                   | 1   | 1           | 1        | 150   |
| 2018 | 1                   | 2   | 1           | 1        | 125   |
| ...  | ...                 | ... | ...         | ...      | ...   |

::: tip TIP
See [the "Database Tables" page](/dev-guide/database/tables.md) in the Developer Guide to learn more about the "BridgePop" table and its columns.
:::

## Command-line Workflow

### Automatically update the "BridgePop" table

1. Start the Dataset Manager on PowerShell

```powershell
p:/data/researchhub-dataset-manager/start

# alternatively:
# cd p:/data/researchhub-dataset-manager
# ./start
```

2. Choose: Update the "population" table in the database (`2 + "Enter"`)
3. Choose: Automatically update all estimates since the latest census year (`1 + "Enter"`)
   - Alternatively, choose: Automatically update the estimates for the latest year only (`2 + "Enter"`)
4. Review the temporary result generated in `/temp/`, i.e. `TempBridgePop.csv`
5. Confirm that the temporary result is as expected (`y + "Enter"`)
6. Restart the process (`y + "Enter"`), or quit the program (`n + "Enter"`)

### Manually update the "BridgePop" table

1. Start the Dataset Manager on PowerShell

```powershell
p:/data/researchhub-dataset-manager/start
```

2. Choose: Update the "population" table in the database (`2 + "Enter"`)
3. Choose: Manually provide input data for population estimates. (`3 + "Enter"`)
4. Place a correctly formated input file in `/input/`
5. Confirm that the input file is in the correct directory (`y + "Enter"`)
6. Review the temporary result generated in `/temp/`, i.e. `TempBridgePop.csv`
7. Confirm that the temporary result is as expected (`y + "Enter"`)
8. Restart the process (`y + "Enter"`), or quit the program (`n + "Enter"`)

## Tutorial

The following example illustrates the process of automatically updating the "BridgePop" table.

In this scenario, the "BridgePop" table is already up-to-date, so the program throws an error.

![Example 2-1](/assets/img/guide_2_1.png)

![Example 2-2](/assets/img/guide_2_2.png)

![Example 2-3](/assets/img/guide_2_3.png)

![Example 2-4](/assets/img/guide_2_4.png)
