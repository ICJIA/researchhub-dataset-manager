# Dataset Output

## Format and contents

Each packaged dataset output is a zipfile (`.zip`) containing multiple files for the actual data as well as relevant metadata. Although the number of data files vary from one packaged dataset to another, in general, each output package is structured as follows:

```
<dataset_name>.zip
├─ <yyyy>_<dataset_name>.csv
└─ metadata.json
```

### Data file

A data comma-seperated values (`.csv`) file is generated using the records saved in the database file. Common to all data files are the following columns:

- `year`: Data year
- `id`: Location (county) ID
- `fips_num`: Location (coutny) Federal Information Processing Standard (FIPS) code
- `county_name`: County name
- `region`: Region of the county (Northern minus Cook, Northern - Cook, Central, or Southern)
- `community_type`: Categorization based on the proportion of rural area in a county
- `percent_rural`: Percentage of rural area in a county
- `population`: Population count

In addition to the common columns, most data files include columns for both raw count values and population-adjusted rate values for relevant data. See the following image for an example of a data file opened in Microsoft Excel:

<img :src="$withBase('/assets/img/data.png')" alt="Data example">

::: warning NOTE
Although the image above shows the file in Microsoft Excel, the file itself is a comma-separated values (`.csv`) text file that can be opened using any text editor, including Notepad.
:::

### Metadata file

A metadata file contains detailed information about the data file in JSON format so that it can be easily uploaded via _Research Hub Studio_.

## List of all datasets

At the time of writing, there are total 32 packaged datasets that are actively maintained and available for the use of the Web Dataset Maintenance Tool to generate automatically.

::: tip TIP
See [the "Data Sources" page](sources.md) to find more about the data sources.
:::

### Based on AOIC data

The following packaged datasets are generated using data from the Administrative Office of the Illinois Courts (AOIC), more specifically, the statistical summary document of its [Annual Report of the Illinois Courts](http://www.illinoiscourts.gov/SupremeCourt/AnnReport.asp).

- **100**: `order_protection`
- **101**: `court_caseload`
- **102**: `court_juvenile_caseload`
- **103**: `felony_sentence`
- **104**: `active_adult_probation_caseload`
- **105**: `active_juvenile_probation_caseload`
- **106**: `juvenile_investigation`
- **107**: `juvenile_petition_continued_under_supervision`
- **108**: `juvenile_adjudication`
- **109**: `juvenile_placement`

### Based on CHRI data

The following packaged datasets are generated using the Criminal History Record Information (CHRI) data from the internal Microsoft SQL Server (`SPAC2SVR`).

- **200**: `juvenile_arrest`

### Based on IDOC data

The following packaged datasets are generated using the Illinois Department of Corrections (IDOC) data from the internal Microsoft SQL Server (`SPAC2SVR`).

- **300**: `idoc_admission`

### Based on IDJJ data

The following packaged datasets are generated using the Illinois Department of Juvenile Justice (IDJJ) data from the internal Microsoft SQL Server (`SPAC2SVR`).

- **400**: `idjj_admission_1316`
- **401**: `idjj_exit_1316`
- **402**: `idjj_admission_1720`
- **403**: `idjj_exit_1720`

### Based on ISP data

The following packaged datasets are generated using [the annual Uniform Crime Report data](http://www.isp.state.il.us/crime/ucrhome.cfm) originally published by the Illinois State Police.

- **500**: `ucr_index_offense`
- **501**: `ucr_index_arrest`
- **502**: `ucr_human_trafficking_offense`
- **503**: `ucr_human_trafficking_arrest`
- **504**: `ucr_drug_arrest`
- **505**: `ucr_domestic_crime_offense`
- **506**: `ucr_hate_crime_offense`
- **507**: `ucr_school_incident`

::: warning NOTE
The ISP's Uniform Crime Report data files for each year often come with corrected values for the previous year's data. The current Web Dataset Maintenance Tool also uses the corrected values for its data outputs whenever possible.
:::

The following package dataset is generated using the Illinois State Police data obtained via email.

- **603**: `drug_submission`

### Based on other data sources

The following packaged datasets come from a variety of other sources.

- **600**: `child_abuse`
- **601**: `county_jail`
- **602**: `juvenile_detention_admission`
- **604**: `elder_abuse`
- **605**: `employment`
- **606**: `illinois_poverty_total`
- **607**: `illinois_poverty_minor`
