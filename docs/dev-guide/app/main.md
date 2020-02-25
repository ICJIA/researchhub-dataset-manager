# `__main__.py`

`__main__.py` is the entrypoint script for the Python app. It defines and runs the `main()` function which contains the core business logic of Research Hub Dataset Manager.

## `main()`

The body of `main()` looks like the following:

```python
def main():
    reset_env(exit=False)

    welcome_msg = "\n### WELCOME TO ICJIA WEB DATASET MAINTENANCE TOOL ###" +\
        "\n\nYou can safely exit this program by typing 'q' and" +\
        "  press Enter whenever asked for your input." +\
        "\n***WARNING: Trying to forcibly quit the program might cause" +\
        " unexpected problems.***" +\
        "\n"
    print(welcome_msg)

    while True:
        task_code = prompt_for_task_input()

        if task_code == '1':
            taks_result = task_data()
        elif task_code == '2':
            taks_result = task_population()
        elif task_code == '3':
            taks_result = task_dataset()

        handle_task_result(taks_result)
```

## Imported `util` functions

`__main__.py` also imports the following functions from the `util` package:

```python
from util import (
  handle_task_result,
  prompt_for_task_input,
  reset_env,
  task_data,
  task_dataset,
  task_population
)
```

- `handle_task_result`
  - Receive the task result and take appropriate actions based on the result (e.g. if success, print success message and ask whether to continue working on a new task).
  - Defined in `util.ui.main`.
- `prompt_for_task_input`
  - Prompt the user to provide input specifying which task to carry out. Possible inputs include `1` for updating "Data", `2` for updating "BridgePop", `3` for generating datasets, and `q` for exiting the program.
  - Defined in `util.ui.prompt`.
- `reset_env`
  - Reset the environment by cleaning out all temporary outputs. If the `exit` input is `True`, an exit message will be printed out at the end.
  - Defined in `util.ui.main`.
- `task_data`
  - Implement business logic for updating the "Data" table in the database. Return `True` if the task is successfully carried out, return `False` otherwise.
  - Defined in `util.ui.main`.
- `task_dataset`
  - Implement business logic for generating packaged dataset products using data stored in the database. Return `True` if the task is successfully carried out, return `False` otherwise.
  - Defined in `util.ui.main`.
- `task_population`
  - Implement business logic for updating the "BridgePop" table in the database. Return `True` if the task is successfully carried out, return `False` otherwise.
  - Defined in `util.ui.main`.
