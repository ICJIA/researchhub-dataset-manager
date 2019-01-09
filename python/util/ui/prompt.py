from util.database.dbread import read_table
from util.ui.misc import complete_choices, handle_exit, prompt_user

def prompt_for_task_input():
    """Prompt for user input for a task to carry out and return the task code."""
    msg = "\nChoose the task you want to carry out:" +\
        "\n- 1 - Update the \"Data\" table in the database." +\
        "\n- 2 - Update the \"BridgePop\" table in the database." +\
        "\n- 3 - Generate a dataset/datasets of your choice."
    
    range_choice = range(1,3+1)
    prompt = "Task to carry out"
    msg, list_choice = complete_choices(msg, range_choice, prompt, back=False)
    errmsg = "ERROR: Invalid choice for task! Try again."
    isvalid = lambda x: x in list_choice

    while True:
        user_input = prompt_user(msg, errmsg, isvalid)
        if user_input == 'q':
            handle_exit()
            continue
        else:
            return user_input

def prompt_for_confirmation(content):
    """Prompt for confirmation for a specificed content."""
    msg = f"\nConfirm if {content} (y) or exit the program (q)." +\
        "\n\n> Confirm? [y/q]"
    errmsg = "ERROR: Invalid response! Try again."
    isvalid = lambda x: x in ['y', 'q']
    
    while True:
        user_input = prompt_user(msg, errmsg, isvalid)
        if user_input == 'q':
            handle_exit()
            continue
        else:
            return True

def prompt_for_group_input(purpose, auto=False):
    """Prompt for user input for dataset group."""
    msg = f'\nSpecify the data group for {purpose}.' +\
        ' Choices for the data group include:'

    dict_group = {
        1: 'Administrative Office of the Illinois Courts (AOIC)',
        2: 'Criminal History Record Information (CHRI)',
        3: 'Illinois Department of Corrections (IDOC)',
        4: 'Illinois Department of Juvenile Justice (IDJJ)',
        5: 'Illinois State Police (ISP)',
        6: 'Other sources'
    }

    range_choice = range(2,6+1) if auto else range(1,6+1)
    for i in range_choice:
        msg += f'\n- {i} - {dict_group[i]}.'

    prompt = "group"
    msg, list_choice = complete_choices(msg, range_choice, prompt)
    errmsg = "ERROR: Invalid choice for group! Try again."
    isvalid = lambda x: x in list_choice

    while True:
        user_input = prompt_user(msg, errmsg, isvalid)
        if user_input == 'q':
            handle_exit()
            continue
        else:
            return user_input

def prompt_for_data_source_input(group):
    """Prompt for user input for dataset source to automatically update the database."""
    msg = f"\nSpecify the data source for updating the database." +\
        " Choices for the data source include:"
    
    if group == 2:
        msg += "\n- 1 - Juvenile arrests (Microsoft SQL Server)."
        range_choice = range(1,1+1)
    elif group == 3:
        msg += "\n- 1 - Prison admissions (Microsoft SQL Server)."
        range_choice = range(1,1+1)
    elif group == 4:
        msg += "\n- 1 - Juvenile court admissions and exits (Microsoft SQL Server)."
        range_choice = range(1,1+1)
    elif group == 5:
        msg += "\n- 1 - Uniform Crime Report (online)."
        range_choice = range(1,1+1)
    elif group == 6:
        msg += "\n- 1 - Illinois County Jail Population (Network drive P:/DATA/JAIL/)." +\
        "\n- 2 - Local Area Unemployment Statistics (Online)." +\
        "\n- 3 - Small Area Income and Poverty Estimates (Online)."
        range_choice = range(1,3+1)
    
    prompt = "Data source"
    msg, list_choice = complete_choices(msg, range_choice, prompt)
    errmsg = "ERROR: Invalid choice for data source! Try again."
    isvalid = lambda x: x in list_choice

    while True:
        user_input = prompt_user(msg, errmsg, isvalid)
        if user_input == 'q':
            handle_exit()
            continue
        else:
            return user_input

def prompt_for_data_input():
    """Prompt for user input for updating method for simplecount estimates."""
    msg = "\nSpecify the method type for updating simplecount table data." +\
        " Choices for the method type include:" +\
        "\n- 1 - Automatically update database records from select data sources." +\
        "\n- 2 - Manually provide input data for updating database records."

    range_choice = range(1, 2+1)
    prompt = "Method type"
    msg, list_choice = complete_choices(msg, range_choice, prompt)
    errmsg = "ERROR: Invalid choice for method type! Try again."
    isvalid = lambda x: x in list_choice
    
    while True:
        user_input = prompt_user(msg, errmsg, isvalid)
        if user_input == 'q':
            handle_exit()
            continue
        else:
            return user_input

def prompt_for_population_input():
    """Prompt for user input for updating method for population estimates."""
    msg = "\nSpecify the method type for updating population data." +\
        " Choices for the method type include:" +\
        "\n- 1 - Automatically update all estimates since the latest census year (recommended)." +\
        "\n- 2 - Automatically update the estimates for the latest year only." +\
        "\n- 3 - Manually provide input data for population estimates."
    
    range_choice = range(1, 2+1)
    prompt = "Method type"
    msg, list_choice = complete_choices(msg, range_choice, prompt)
    errmsg = "ERROR: Invalid choice for method type! Try again."
    isvalid = lambda x: x in list_choice
    
    while True:
        user_input = prompt_user(msg, errmsg, isvalid)
        if user_input == 'q':
            handle_exit()
            continue
        else:
            return user_input

def prompt_for_dataset_input(group):
    """Prompt for user input for generating packaged output datasets."""
    msg = "\nProvide the choice of the dataset package to generate or exit the program (q)."
    
    dataset = read_table('Dataset')
    
    dict_dataset = dataset[dataset['group'] == group] \
        .set_index('id') \
        .to_dict()['name']

    range_choice = range(min(dict_dataset.keys()), max(dict_dataset.keys()) + 1)

    for i in range_choice:
        msg += f"\n- {i} - Dataset: {dict_dataset[i]}."
    
    prompt = "Dataset to generate"
    if group in [1, 4, 5]:
        msg, list_choice = complete_choices(msg, range_choice, prompt, all=True)
    else:
        msg, list_choice = complete_choices(msg, range_choice, prompt)
    errmsg = "ERROR: Invalid dataset choice! Try again."
    isvalid = lambda x: x in list_choice
    
    while True:
        user_input = prompt_user(msg, errmsg, isvalid)
        if user_input == 'q':
            handle_exit()
            continue
        else:
            return user_input

def prompt_for_new_task(success=True):
    """Prompt for user input for continuing to carry out a new task."""
    if success:
        msg_intro = "NOTE: Congratulations! Your task is successfully completed!"
    else:
        msg_intro = "NOTE: The program could not finish the task." +\
            " All intermediary results will be abandoned." +\
            " Please check your input before retrying."
    msg = "\nYou may continue to carry out another task (y)" +\
        " or exit the program (n)." +\
        "\n\n> Continue? [y/n]"
    errmsg = "ERROR: Invalid response! Try again."
    isvalid = lambda x: x in ['y', 'n']

    print(msg_intro)
    user_input = prompt_user(msg, errmsg, isvalid)
    if user_input == 'y':
        return
    else:
        raise SystemExit