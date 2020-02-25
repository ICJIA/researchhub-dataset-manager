# 3. Generate dataset

You can use Research Hub Dataset Manager to easily generate packaged dataset outputs in the zipfile format base on the updated records in the database. Generate dataset zipfiles are stored in `/dataset/`.

::: tip TIP
See [the "Dataset Output" page](/guide/output.md) to find a list of datasets that can be generated using the Dataset Manager.
:::

## Command-line Workflow

1. Start the Dataset Manager on PowerShell

```powershell
p:/data/researchhub-dataset-manager/start

# alternatively:
# cd p:/data/researchhub-dataset-manager
# ./start
```

2. Choose: "- 3 - Generate a dataset/datasets of your choice." (`3 + "Enter"`)
3. Specify the data source group for generating datasets (`<input> + "Enter"`)
4. Choose the dataset package to generate (`<input> + "Enter"`)
5. Restart the process (`y + "Enter"`), or quit the program (`n + "Enter"`)

## Tutorial

The following example illustrates the process of generating the `ucr_index_offense` dataset output using the command-line interface to the WDM Tool.

In this scenario, the dataset is successfully generated and stored in `/datasets/`. The user then chooses to continue to the next task.

<img :src="$withBase('/assets/img/guide_3_1.png')" alt="Example 3-1">

<img :src="$withBase('/assets/img/guide_3_2.png')" alt="Example 3-2">

<img :src="$withBase('/assets/img/guide_3_3.png')" alt="Example 3-3">

<img :src="$withBase('/assets/img/guide_3_4.png')" alt="Example 3-4">

<img :src="$withBase('/assets/img/guide_3_5.png')" alt="Example 3-5">
