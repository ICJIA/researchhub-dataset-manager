# Data Sources

::: tip TIP
Bold-font numbers in the rest of this section correspond to the ID value of the "Variable" table in the database file.

See [the "Database" section](/dev-guide/database/) to learn more about the database tables.
:::

::: tip TIP
The first three digits of the "Variable" ID value corresponds to the "Dataset" ID value. For instance, the Variable ID `10000` is the first variable in the Dataset ID `100`.

See [the "Dataset Output" page](/guide/output.md) in the Guide to view the dataset list.
:::

## National Vital Statistics System:

The "BridgePop" table records are drawn from [U.S. Census Populations With Bridged Race Categories](https://www.cdc.gov/nchs/nvss/bridged_race.htm) by the National Vital Statistics System. The Bridged-Race Population Estimates data files are available [here](https://www.cdc.gov/nchs/nvss/bridged_race/data_documentation.htm).

## Admin. Office of the Illinois Courts

Each year, AOIC publishes online [_Annual Report of the Illinois Courts_](http://www.illinoiscourts.gov/SupremeCourt/AnnReport.asp). Its _Statistical Summary_ document contains many data tables providing values for the "Data" table in the Dataset Manager's database.

#### Table: Civil and Domestic Relations Caseload Statistics by County Circuit Courts of Illinois

- **10000**: `DOMESTIC RELATIONS/ORDER OF PROTECTION` value

#### Table: Criminal and Quasi-Criminal Caseload Statistics by County Circuit Courts of Illinois

- **10100**: `New filed` value of `CRIMINAL/FELONY` column
- **10101**: `New filed` value of `CRIMINAL/MISDEMEANOR` column
- **10102**: `New filed` value of `CRIMINAL/DUI` column
- **10109**: `New filed` value of `CRIMINAL/TOTAL ALL CASES` column

#### Table: Juvenile Caseload Statistics by County Circuit Courts of Illinois

- **10200**: `New filed` value of `ABUSE & NEGLECT` column
- **10201**: `New filed` value of `DELINQUENCY` column
- **10202**: `New filed` value of `OTHER` column

#### Table: Felony Dispositions and Sentences by County Circuit Courts of Illinois

- **10300**: sum of `SENTENCES/STATE IMPRISONMENT` and `SENTENCES/DEATH #` values.
- **10301**: `SENTENCES/PROBATION` value
- **10302**: `SENTENCES/DEATH #` value
- **10303**: `SENTENCES/OTHER` value

#### Table: Active Adult Caseload

- **10400**: `Felony` value
- **10401**: `Misd.` value
- **10402**: `DUI` value
- **10403**: `Traffic` value
- **10404**: `Total` value
- **10405**: `Admin.` value

#### Table: Active Juvenile Caseload

- **10500**: `Probation` value
- **10501**: `Supervision` value
- **10502**: `CUS` value
- **10503**: `Informal` value
- **10504**: `Admin.` value
- **10505**: `Other` value

#### Table: Juvenile Investigations Report

- **10600**: `Social History` value
- **10601**: `Supplemental Social Hist.` value
- **10602**: `Intake Screening` value
- **10603**: `Other` value

#### Table: Juvenile Petitions Continued Under Supervision/Adjudications

- **10700**: `Continued Under Supervision/Delinquency` value
- **10701**: _Discontinued_
- **10702**: _Discontinued_
- **10703**: `Continued Under Supervision/Truancy` value

* **10800**: `Adjudications/Delinquency` value
* **10801**: _Discontinued_
* **10802**: _Discontinued_
* **10803**: `Adjudications/Truancy` value

#### Table: Juvenile Placements

- **10900**: sum of `Place in Foster Home/In State` and `Place in Foster Home/Out of State` values
- **10901**: sum of `Placed in Group Home/In State` and `Placed in Group Home/Out of State` values
- **10902**: sum of `Placed in Treatment/In State` and `Placed in Treatment/Out of State` values
- **10903**: sum of `Placed in Relative/In State` and `Placed in Relative/Out of State` values

## R&A Microsoft SQL Server

The following data are drawn from ICJIA R&A's Microsoft SQL Server (`SPAC2SRV`) databases.

If you are curious about the SQL Server databases, contact Ernst Melchoir (Computer Support Specialist, [Ernst.Melchior@illinois.gov](mailto:Ernst.Melchior@illinois.gov)) for more information.

### Criminal History Record Information (CHRI)

The latest CHRI data pulled from the live server are stored in an ICJIA R&A's Microsoft SQL Server database, named `AnnualPulls`.

#### Table `AnnualPulls.dbo.Arrests`

- **20000**: count of rows filtered by the age (juvenile only)

### Illinois Department of Corrections (IDOC)

The latest IDOC data are stored in an ICJIA R&A's Microsoft SQL Server (`SPAC2SRV`) database, named `PrisonMain`.

::: warning NOTE
Aggregating `PrisonMain.dbo.PrisonAdmits` counts is based on fiscal years. Use the `FiscalYr` values for this.
:::

#### Table `PrisonMain.dbo.PrisonAdmits`

- **30000**: count of rows with `ADMTYPO3 == 1`
- **30001**: count of rows with `ADMTYPO3 == 2`
- **30002**: count of rows in **30000** where `OFFTYPE2 == 1`
- **30003**: count of rows in **30000** where `OFFTYPE2 == 2`
- **30004**: count of rows in **30000** where `OFFTYPE2 == 4`
- **30005**: count of rows in **30000** where `OFFTYPE2 in (3.1, 3.2, 3.3, 3.4, 3.5, 3.6)`
- **30006**: count of rows in **30000** where `OFFTYPE2 in (0, 3, 5, 7)`
- **30007**: count of rows in **30000** where `OFFTYPE3 == 1`
- **30008**: count of rows in **30000** where `SEX != F`
- **30009**: count of rows in **30000** where `SEX == F`

### Illinois Department of Juvenile Justice (IDJJ)

The latest IDJJ data are stored in an ICJIA R&A's Microsoft SQL Server (`SPAC2SRV`) database, named `PrisonMain`.

::: warning NOTE
Aggregating `PrisonMain.dbo.IDJJ_Admissions` and `PrisonMain.dbo.IDJJ_Exits` counts is based on fiscal years. Use the `SFY` values for this.
:::

#### Table `PrisonMain.dbo.IDJJ_Admissions`

##### (Age 13 to 16)

- **40000**: count of rows with `Age in (13, 16)` and `admtypo in (CE, CER, DR, IC, MVN, PVN, RAM)`
- **40001**: count of rows with `Age in (13, 16)` and `admtypo == CE`
- **40002**: count of rows with `Age in (13, 16)` and `admtypo in (TMV, TPV)`
- **40003**: count of rows in **40000** where `sex == M`
- **40004**: count of rows in **40000** where `sex != M`
- **40005**: count of rows in **40000** where `race == WHI`
- **40006**: count of rows in **40000** where `race == BLK`
- **40007**: count of rows in **40000** where `race == HSP`
- **40008**: count of rows in **40000** where `OFFTYPE9 == 1`
- **40009**: count of rows in **40000** where `OFFTYPE9 == 2`
- **40010**: count of rows in **40000** where `OFFTYPE9 == 3`
- **40011**: count of rows in **40000** where `OFFTYPE9 == 4`
- **40012**: count of rows in **40000** where `OFFTYPE9 == 5`
- **40013**: count of rows in **40000** where `hclass in (M, X, 1, 2, 3, 4)`
- **40014**: count of rows in **40000** where `hclass not in (M, X, 1, 2, 3, 4)`

##### (Age 17 to 20)

- **40200**: count of rows with `Age in (17, 20)` and `admtypo in (CE, CER, DR, IC, MVN, PVN, RAM)`
- **40201**: count of rows with `Age in (17, 20)` and `admtypo == CE`
- **40202**: count of rows with `Age in (17, 20)` and `admtypo in (TMV, TPV)`
- **40203**: count of rows in **40200** where `sex == M`
- **40204**: count of rows in **40200** where `sex != M`
- **40205**: count of rows in **40200** where `race == WHI`
- **40206**: count of rows in **40200** where `race == BLK`
- **40207**: count of rows in **40200** where `race == HSP`
- **40208**: count of rows in **40200** where `OFFTYPE9 == 1`
- **40209**: count of rows in **40200** where `OFFTYPE9 == 2`
- **40210**: count of rows in **40200** where `OFFTYPE9 == 3`
- **40211**: count of rows in **40200** where `OFFTYPE9 == 4`
- **40212**: count of rows in **40200** where `OFFTYPE9 == 5`
- **40213**: count of rows in **40200** where `hclass in (M, X, 1, 2, 3, 4)`
- **40214**: count of rows in **40200** where `hclass not in (M, X, 1, 2, 3, 4)`

#### Table `PrisonMain.dbo.IDJJ_Exits`

##### (Age 13 to 16)

- **40100**: count of rows with `ExitAge in (13, 16)` and `admtypo in (CE, CER, DR, IC, MVN, PVN, RAM)`
- **40101**: count of rows with `ExitAge in (13, 16)` and `admtypo == CE`
- **40102**: count of rows with `ExitAge in (13, 16)` and `admtypo in (TMV,TPV)`
- **40103**: count of rows in **40100** where `sex == M`
- **40104**: count of rows in **40100** where `sex != M`
- **40105**: count of rows in **40100** where `race == WHI`
- **40106**: count of rows in **40100** where `race == BLK`
- **40107**: count of rows in **40100** where `race == HSP`
- **40108**: count of rows in **40100** where `OFFTYPE9 == 1`
- **40109**: count of rows in **40100** where `OFFTYPE9 == 2`
- **40110**: count of rows in **40100** where `OFFTYPE9 == 3`
- **40111**: count of rows in **40100** where `OFFTYPE9 == 4`
- **40112**: count of rows in **40100** where `OFFTYPE9 == 5`
- **40113**: count of rows in **40100** where `hclass in (M, X, 1, 2, 3, 4)`
- **40114**: count of rows in **40100** where `hclass not in (M, X, 1, 2, 3, 4)`

##### (Age 17 to 20)

- **40300**: count of rows with `ExitAge in (17, 20)` and `admtypo in (CE, CER, DR, IC, MVN, PVN, RAM)`
- **40301**: count of rows with `ExitAge in (17, 20)` and `admtypo == CE`
- **40302**: count of rows with `ExitAge in (17, 20)` and `admtypo in (TMV,TPV)`
- **40303**: count of rows in **40300** where `sex == M`
- **40304**: count of rows in **40300** where `sex != M`
- **40305**: count of rows in **40300** where `race == WHI`
- **40306**: count of rows in **40300** where `race == BLK`
- **40307**: count of rows in **40300** where `race == HSP`
- **40308**: count of rows in **40300** where `OFFTYPE9 == 1`
- **40309**: count of rows in **40300** where `OFFTYPE9 == 2`
- **40310**: count of rows in **40300** where `OFFTYPE9 == 3`
- **40311**: count of rows in **40300** where `OFFTYPE9 == 4`
- **40312**: count of rows in **40300** where `OFFTYPE9 == 5`
- **40313**: count of rows in **40300** where `hclass in (M, X, 1, 2, 3, 4)`
- **40314**: count of rows in **40300** where `hclass not in (M, X, 1, 2, 3, 4)`

## Illinois State Police - Uniform Crime Reports

The State Police releases annual Uniform Crime Reports [here](http://www.isp.state.il.us/crime/ucrhome.cfm). Currently, each year's report comes with four datasets.

::: warning NOTE
`<yy>` in the column names represent the last two digits of the latest year.
:::

#### File: Index Crime Offense & Drug Arrest Data

##### (Index crime offenses)

- **50000**: `CH<yy>` value
- **50001**: `Rape<yy>` value
- **50002**: `Rob<yy>` value
- **50003**: `AggBA<yy>` value
- **50004**: `Theft<yy>` value
- **50005**: `Burg<yy>` value
- **50006**: `MVT<yy>` value
- **50007**: `Arson<yy>` value

##### (Index crime arrests)

- **50100**: `ACH<yy>` value
- **50101**: `Arape<yy>` value
- **50102**: `Arob<yy>` value
- **50103**: `AAggBA<yy>` value
- **50104**: `Atheft<yy>` value
- **50105**: `Aburg<yy>` value
- **50106**: `Amvt<yy>` value
- **50107**: `Aarson<yy>` value

##### (Human trafficking offenses)

- **50200**: `HTsex<yy>` value
- **50201**: `HTserve<yy>` value

##### (Human trafficking arrests)

- **50300**: `aHTsex<yy>` value
- **50301**: `aHTserve<yy>` value

##### (Drug arrests)

- **50400**: `Acca<yy>` value
- **50401**: `Acsa<yy>` value
- **50402**: `Ahsna<yy>` value
- **50403**: `Adpa<yy>` value
- **50404**: `Ameth<yy>` value

#### File: Domestic Offenses Data

- **50500**: `Domestic<yy>` value

#### File: Hate Crime Incidents Data

- **50600**: `Hate<yy>` value

#### File: School Incidents Data

- **50700**: Sum of `ch<yy>`, `csa<yy>`, `aggbatt<yy>`, `batt<yy>`, `aggasslt<yy>`, `assault<yy>`, and `intimidation<yy>` values
- **50701**: _Discontinued as of 2014_

## Other sources

### Illinois Department of Children and Family Services

Child abuse related data are drawn from [Child Abuse and Neglect Statistics by Illinois Department of Children and Family Services](https://www2.illinois.gov/dcfs/aboutus/newsandreports/reports/Pages/default.aspx), especially tables 7, 8, 19, 20 of the Annual Statistical Report.

"Children" is defined as age <= 17. See the latest example, [the fiscal year 2015 report](https://www2.illinois.gov/dcfs/aboutus/newsandreports/Documents/DCFS_Annual_Statistical_Report_FY2015.pdf).

#### Table 7: County Distribution of Alleged Victims of Abuse and Neglect

- **60000**: `Number Children` value

#### Table 8: County Distribution of Indicated Victims of Abuse and Neglect

- **60001**: `Number Children` value

#### Table 19: County Distribution of Alleged Victims of Sexual Abuse

- **60002**: `Number Children Reported` value

#### Table 20: County Distribution of Alleged Victims of Sexual Abuse

- **60003**: `Number Children` value

### IDOC - Jail and Detention Standards

Jail and Detention Standards data are obtained directly from the source via email and stored in `P:/DATA/JAIL/`. Use data in `yyyy ICJIA County SUP Totals.xls` files. Some of the old data come from `Jailpop.xls`. Cook county has a separate data source: [CAFR](https://www.cookcountyil.gov/service/financial-reports).

- **60100**: average of `Average Monthly Pop` per county
- **60101**: sum of `TOTAL Number of Bookings` per county

### ISP - Drug seizures and submissions

Drug seizures and submissions data are obtained directly from the source via email and stored in `P:/DATA/DRUG/`. In particular, the original data files are stored in a subdirectory, `/Miscellany/Monthly drug lab submissions by county/`.

Contact Idetta Phillips (Research Analyst, [Idetta.Phillips@illinois.gov](mailto:Idetta.Phillips@Illinois.gov)) for more information.

#### File: SPIntell \<mm\>\<yy\>.dbf

- **60300**: Sum of `ENTRIES` values where `DRUGTYPE` is `AM`
- **60301**: Sum of `ENTRIES` values where `DRUGTYPE` is `BB`
- **60302**: Sum of `ENTRIES` values where `DRUGTYPE` is `CA`
- **60303**: Sum of `ENTRIES` values where `DRUGTYPE` is `CO`
- **60304**: Sum of `ENTRIES` values where `DRUGTYPE` is `LS`
- **60305**: Sum of `ENTRIES` values where `DRUGTYPE` is `MO`
- **60306**: Sum of `ENTRIES` values where `DRUGTYPE` is `NS`
- **60307**: Sum of `ENTRIES` values where `DRUGTYPE` is `OD`
- **60308**: Sum of `ENTRIES` values where `DRUGTYPE` is `OH`
- **60309**: Sum of `ENTRIES` values where `DRUGTYPE` is `OP`
- **60310**: Sum of `ENTRIES` values where `DRUGTYPE` is `OS`
- **60311**: Sum of `ENTRIES` values where `DRUGTYPE` is `PC`
- **60312**: Sum of `ENTRIES` values where `DRUGTYPE` is `SN`
- **60313**: Sum of `ENTRIES` values where `DRUGTYPE` is `ST`
- **60314**: Sum of `ENTRIES` values where `DRUGTYPE` is `HR`
- **60315**: Sum of `ENTRIES` values where `DRUGTYPE` is `CP`
- **60316**: Sum of `ENTRIES` values where `DRUGTYPE` is `CN`
- **60317**: Sum of `ENTRIES` values where `DRUGTYPE` is `PR`
- **60318**: Sum of `ENTRIES` values where `DRUGTYPE` is `OT`

### Illinois Department of Againg

Historical elder abuse data are obtained directly from the source via email and stored in `P:/DATA/Elder Abuse/`. This dataset has not been updated for a while and may be discontinued in future.

- **60400**: Value for the relevant year.

### Illinois Department of Employment

County-level unemployment data are drawn from [Local Area Unemployment Statistics (LAUS)](http://www.ides.illinois.gov/LMI/Pages/Local_Area_Unemployment_Statistics.aspx) by the Illinois Department of Employment. See the latest example, [2017 report](http://www.ides.illinois.gov/LMI/Local%20Area%20Unemployment%20Statistics%20LAUS/historical/2017-moaa.xls).

#### Local Area Unemployment Statistics Table

- **60500**: `LABOR FORCE` value where `MONTH#` is 13 (annual average)
- **60501**: `UNEMPLOYED NUMBER` value where `MONTH#` is 13 (annual average)
- **60502**: `EMPLOYED` value where `MONTH#` is 13 (annual average)

### U.S. Census Bureau

Illinois poverty estimates data are drawn from [Small Area Income and Poverty Estimates (SAIPE)](https://www.census.gov/programs-surveys/saipe.html). The actual datasets can be found [here](https://www2.census.gov/programs-surveys/saipe/datasets/). Also, see the layout [documentation](https://www2.census.gov/programs-surveys/saipe/technical-documentation/file-layouts/state-county/2016-estimate-layout.txt) for more information.

#### File: /\<yyyy\>/\<yyyy\>-state-and-county/est\<yy\>-il.txt

- **60600**: characters 8-15 (Estimate of people of all ages in poverty)
- **60700**: characters 50-57 (Estimate of people age 0-17 in poverty)
