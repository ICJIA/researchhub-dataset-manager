# Prerequisites

::: warning NOTE
Make sure to read the current page and follow all the steps below _prior to_ trying Research Hub Dataset Manager.
:::

## Download and install Python via Anaconda

### What is Python?

![Python logo](https://www.python.org/static/community_logos/python-logo-generic.svg)

Python is a popular programming language that is easy to learn and ideal for a variety of projects. The following is an excerpt from ["What is Python? Executive Summary" by Python Software Foundation](https://www.python.org/doc/essays/blurb/):

> _"Python is an interpreted, object-oriented, high-level programming language with dynamic semantics. [...] Python's simple, easy to learn syntax emphasizes readability and therefore reduces the cost of program maintenance. Python supports modules and packages, which encourages program modularity and code reuse. The Python interpreter and the extensive standard library are available in source or binary form without charge for all major platforms, and can be freely distributed."_

Since ICJIA Research Hub Dataset Manager is a program written in Python at its core, you must first install Python on your computer in order to use the Dataset Manager.

::: warning NOTE
This might change in future with the Dataset Manager later being complied into a Windows executabe (.exe) file to eliminate the need to install Python if possible. If you would like to try compiling the program on your own, take a look at [the PyInstaller documentation](http://www.pyinstaller.org/).
:::

### Download and install

Go to [the download page for Python](https://www.python.org/downloads/). Click the Download button for the latest available version of Python (3.8.1 version at the time of writing). This will start the downloading process.

Once complete, navigate to the download location, usually the Downloads folder for a Windows PC (`C:\Users\<username>\Downloads`). You will find the installer with a name such as `python-3.8.1.exe`. Run the installer and follow the instructions to complete the installation.

**Make sure to allow the Installer to add Python to PATH!**

::: warning NOTE
Installing a new program on your PC will require Administrator Permission. You must talk to the DoIT staff to help you on installation.
:::

## Add Python to PATH

In order to access Python from anywhere using a command-line tool, such as Command Prompt or Windows PowerShell, it is necessary to add Python to the "PATH" environmental variable.

Ideally, you added Python to PATH during the installation process. But if you missed it, there is a way to get this done manually.

First, go to Start and search for "Edit environmental variables for your account." Then choose "Path" or "PATH" variable, click "Edit" button, and add to the variable the following two locations (i.e. paths):

- `C:\Users\<username>\AppData\Local\Programs\Python\Python38-32`
- `C:\Users\<username>\AppData\Local\Programs\Python\Python38-32\scripts`

::: warning NOTE
You must be logged on with your personal account when editing the PATH environmental variable.
:::

Once you apply the change, Python should be accessible from anywhere on your PC. You may test this by opening a command-line tool, and execute `python --version` as in the following image:

<img :src="$withBase('/assets/img/prerequisites_1.png')" alt="Microsoft Powershell screenshot">

If the relevant output is printed without causing any error, Python is successfully added to PATH.

::: tip TIP
This documentation recommends using Windows Powershell for running the Dataset Manager although other command-line tools (e.g. Commend Prompt or Git Bash) can run the program just the same.

You can open PowerShell anywhere on the PC. Simply hold a `Shift` key, press the right mouse button (right click), and choose the "Open PowerShell window here" option.
:::

## Set up the P:\ network drive

The current documentation assumes that you have access to the `\\MAINFILESRV` network drive, which serves as a main storage for the R&A Unit and is conventionally mapped to `P:\` on a staff member's workstation. In fact, the Dataset Manager for the official use is located at the `P:\DATA\researchhub-data-manager\` directory.

Therefore, before proceeding to the rest of the documentation, make sure you have access to `\\MAINFILESRV\r&a\` and the network drive is correctly mapped to `P:\`. Contact the DoIT staff for help if needed.
