# Getting Started

::: warning NOTE
Make sure to take all the steps in [the previous "Prerequisites" page](prerequisites.md) prior to following the steps below.
:::

## Start the Dataset Manager app

The Research Hub Dataset Manager app is a Python program located at `P:\DATA\researchhub-dataset-manager`.

To start the app, open up Windows PowerShell and run the following command:

```powershell
> p:/data/researchhub-dataset-manager/start
```

Alternatively, you can first move to the directory where the program is stored and run the program using the following command:

```powershell
> cd p:/data/researchhub-dataset-manager
> ./start
```

::: tip TIP
`cd <path>` is a Windows PowerShell command you can use to move to a location specificed by the path. To learn more about Windows Powershell, visit [the official documentation website](https://docs.microsoft.com/en-us/powershell/) by Microsoft.
:::

Either way, the `.\start` command will execute the program. After a few seconds, the interface to the Dataset Manager will appear as shown in the following image:

<img :src="$withBase('/assets/img/screenshot.png')" alt="Microsoft Powershell screenshot">

**Congratulations**:tada: Now you are ready to get some work done!

## Interact with the app

The Dataset Manager app has an interface designed to first receive a user input and then carry out appropriate tasks. Therefore, at each step, it will ask you for an input with possible options and wait.

You can provide the Dataset Manager app with an input by typing the number or character that matches the desired task and hit `<Enter>` so that the Dataset Manager app knows what it is supposed to do.

Once you submit your input by hitting that `<Enter>` button, the Dataset Manager will move on to the next step, which might require additional inputs from you. Simply follow along the instructions on the screen to get the desired result, i.e. updating its database with new records or generating packaged dataset product.

::: tip TIP
You will find out more about which tasks the current Tool can carry out and how the interface would look like for those tasks in [the following "Tasks" pages](tasks/).
:::

## Safely exit the program

::: danger WARNING
Trying to forcibly quit the program might cause unexpected problems!
:::

At each step, the Dataset Manager app offers an input option to safely exit the program, ususally with the `q` input.

Although it is possible to forcibly quit the program (e.g. by manually closing the PowerShell window or exiting the program from Task Manager), such an action might lead to erroneous behaviors, which may include failing to clean up temporary outputs in the database or to finish updating the database file.

Therefore, it is _strongly recommended_ that you exit the program using the provided interface by `q + <Enter>` or other appropriate option.
