"""Offer functions for user interface.

This module offer functions to prompt for and handle user inputs.
The module depends on the ``database`` module.

The module contains the following public functions to be called externally:

``prompt_for_task_input()`` prompts the user for the task to carry out. 
``prompt_for_confirmation()`` prompts the user for confirmation for a specified content.
``prompt_for_source_group_input()`` prompt for user inputs for dataset source group..
``prompt_for_data_source_input()`` prompt for user inputs for dataset source to automatically update the database..
``prompt_for_simplecount_input()`` prompt for user inputs for updating method for simplecount estimates..
``prompt_for_population_input()`` prompt for user inputs for updating method for population estimates..
``prompt_for_dataset_package_input()`` prompt for user input for generating packaged output datasets.
``prompt_for_new_task()`` prompts for user input for continuing to carry out a new task.
"""
from time import sleep

from . import database

def _prompt(msg, errmsg, isvalid):
    """Prompt for input given a message and return that value after verifying the input.

    Args:
        msg (str): Message to show when asking for user input.
        errmsg (str): Message to show if user input is invalid.
        isvalid (function): Returns True if user input is valid.
    """
    user_input = None
    while user_input is None:
        user_input = input(f'{msg}: ').strip().lower()
        if not isvalid(user_input):
            print(f'{errmsg}\n')
            sleep(.300)
            user_input = None
    sleep(.300)
    return user_input

def _complete_choices(msg, choice_range, prompt, all=False, back=True):
    """Return the complete message and choice list.""" 
    choice_list = [str(i) for i in choice_range]
    
    if all:
        choice_list += ['a']
        msg += '\n- a - All of the above.'

    if back:
        choice_list += ['b']
        msg += '\n- b - Back to the main menu.'
    
    choice_list += ['q']
    msg += f'\n- q - Exit the program.\n\n> {prompt}? [{"/".join(choice_list)}]'

    return msg, choice_list

def _exit_handler():
    msg = '\nAre you sure you wish to exit the program?' +\
        ' All intermediary results will be abandoned.' +\
        '\n\n> Exit? [y/n]'
    errmsg = 'ERROR: Invalid response! Try again.'
    isvalid = lambda x: x in ['y', 'n']
    
    exit_input = _prompt(msg, errmsg, isvalid)
    if exit_input == 'y':
        raise SystemExit
    else:
        pass

def prompt_for_task_input():
    """Prompt for user input for a task to carry out and return the task code."""
    msg = '\nChoose the task you want to carry out:' +\
        '\n- 1 - Update the "simplecount" table in the database.' +\
        '\n- 2 - Update the "population" table in the database.' +\
        '\n- 3 - Generate a dataset/datasets of your choice.'
    
    choice_range = range(1,3+1)
    prompt = 'Task to carry out'
    msg, choice_list = _complete_choices(msg, choice_range, prompt, back=False)
    errmsg = 'ERROR: Invalid choice for task! Try again.'
    isvalid = lambda x: x in choice_list

    while True:
        user_input = _prompt(msg, errmsg, isvalid)
        if user_input == 'q':
            _exit_handler()
            continue
        else:
            return user_input

def prompt_for_confirmation(content):
    """Prompt for confirmation for a specificed content."""
    msg = f'\nConfirm if {content} (y) or exit the program (q).' +\
        '\n\n> Confirm? [y/q]'
    errmsg = 'ERROR: Invalid response! Try again.'
    isvalid = lambda x: x in ['y', 'q']
    
    while True:
        user_input = _prompt(msg, errmsg, isvalid)
        if user_input == 'q':
            _exit_handler()
            continue
        else:
            return True

def prompt_for_source_group_input(purpose, auto=False):
    """Prompt for user input for dataset source group."""
    msg = f'\nSpecify the data source group for {purpose}.' +\
        ' Choices for the data source group include:'

    source_group_dict = {
        1: 'Administrative Office of the Illinois Courts (AOIC)',
        2: 'Criminal History Record Information (CHRI)',
        3: 'Illinois Department of Corrections (IDOC)',
        4: 'Illinois Department of Juvenile Justice (IDJJ)',
        5: 'Illinois State Police (ISP)',
        6: 'Other sources'
    }

    choice_range = range(2,6+1) if auto else range(1,6+1)
    for i in choice_range:
        msg += f'\n- {i} - {source_group_dict[i]}.'

    prompt = 'Source group'
    msg, choice_list = _complete_choices(msg, choice_range, prompt)
    errmsg = 'ERROR: Invalid choice for source group! Try again.'
    isvalid = lambda x: x in choice_list

    while True:
        user_input = _prompt(msg, errmsg, isvalid)
        if user_input == 'q':
            _exit_handler()
            continue
        else:
            return user_input

def prompt_for_data_source_input(source_group):
    """Prompt for user input for dataset source to automatically update the database."""
    msg = f'\nSpecify the data source for updating the database.' +\
        ' Choices for the data source include:'
    
    if source_group == 2:
        msg += '\n- 1 - Juvenile arrests (Microsoft SQL Server).'
        choice_range = range(1,1+1)
    elif source_group == 3:
        msg += '\n- 1 - Prison admissions (Microsoft SQL Server).'
        choice_range = range(1,1+1)
    elif source_group == 4:
        msg += '\n- 1 - Juvenile court admissions and exits (Microsoft SQL Server).'
        choice_range = range(1,1+1)
    elif source_group == 5:
        msg += '\n- 1 - Uniform Crime Report (online).'
        choice_range = range(1,1+1)
    elif source_group == 6:
        msg += '\n- 1 - Illinois County Jail Population (Network drive P:/DATA/JAIL/).' +\
        '\n- 2 - Local Area Unemployment Statistics (Online).' +\
        '\n- 3 - Small Area Income and Poverty Estimates (Online).'
        choice_range = range(1,3+1)
    
    prompt = 'Data source'
    msg, choice_list = _complete_choices(msg, choice_range, prompt)
    errmsg = 'ERROR: Invalid choice for data source! Try again.'
    isvalid = lambda x: x in choice_list

    while True:
        user_input = _prompt(msg, errmsg, isvalid)
        if user_input == 'q':
            _exit_handler()
            continue
        else:
            return user_input

def prompt_for_simplecount_input():
    """Prompt for user input for updating method for simplecount estimates."""
    msg = '\nSpecify the method type for updating simplecount table data.' +\
        ' Choices for the method type include:' +\
        '\n- 1 - Automatically update database records from select data sources.' +\
        '\n- 2 - Manually provide input data for updating database records.'

    choice_range = range(1, 2+1)
    prompt = 'Method type'
    msg, choice_list = _complete_choices(msg, choice_range, prompt)
    errmsg = 'ERROR: Invalid choice for method type! Try again.'
    isvalid = lambda x: x in choice_list
    
    while True:
        user_input = _prompt(msg, errmsg, isvalid)
        if user_input == 'q':
            _exit_handler()
            continue
        else:
            return user_input

def prompt_for_population_input():
    """Prompt for user input for updating method for population estimates."""
    msg = '\nSpecify the method type for updating population data.' +\
        ' Choices for the method type include:' +\
        '\n- 1 - Automatically update all estimates since the latest census year (recommended).' +\
        '\n- 2 - Automatically update the estimates for the latest year only.' +\
        '\n- 3 - Manually provide input data for population estimates.'
    
    choice_range = range(1, 2+1)
    prompt = 'Method type'
    msg, choice_list = _complete_choices(msg, choice_range, prompt)
    errmsg = 'ERROR: Invalid choice for method type! Try again.'
    isvalid = lambda x: x in choice_list
    
    while True:
        user_input = _prompt(msg, errmsg, isvalid)
        if user_input == 'q':
            _exit_handler()
            continue
        else:
            return user_input

def prompt_for_dataset_package_input(source_group):
    """Prompt for user input for generating packaged output datasets."""
    msg = '\nProvide the choice of the dataset package to generate or exit the program (q).'
    
    database.init()
    package = database.fetch_table('package')
    package_dict = package.set_index('id').to_dict()['name']
    
    if source_group == 1:
        choice_range = range(1, 8+1)
    elif source_group == 2:
        choice_range = range(9, 9+1)
    elif source_group == 3:
        choice_range = range(10, 10+1)
    elif source_group == 4:
        choice_range = range(11, 12+1)
    elif source_group == 5:
        choice_range = range(13, 18+1)
    elif source_group == 6:
        choice_range = range(19, 26+1)

    for i in choice_range:
        msg += f'\n- {i} - Dataset: {package_dict[i]}.'
    
    prompt = 'Dataset to generate'
    if source_group in [1, 4, 5]:
        msg, choice_list = _complete_choices(msg, choice_range, prompt, all=True)
    else:
        msg, choice_list = _complete_choices(msg, choice_range, prompt)
    errmsg = 'ERROR: Invalid dataset choice! Try again.'
    isvalid = lambda x: x in choice_list
    
    while True:
        user_input = _prompt(msg, errmsg, isvalid)
        if user_input == 'q':
            _exit_handler()
            continue
        else:
            return user_input

def prompt_for_new_task(success=True):
    """Prompt for user input for continuing to carry out a new task."""
    if success:
        msg_intro = 'NOTE: Congratulations! Your task is successfully completed!'
    else:
        msg_intro = 'NOTE: The program could not finish the task.' +\
            ' All intermediary results will be abandoned.' +\
            ' Please check your input before retrying.'
    msg = '\nYou may continue to carry out another task (y)' +\
        ' or exit the program (n).' +\
        '\n\n> Continue? [y/n]'
    errmsg = 'ERROR: Invalid response! Try again.'
    isvalid = lambda x: x in ['y', 'n']

    print(msg_intro)
    user_input = _prompt(msg, errmsg, isvalid)
    if user_input == 'y':
        return
    else:
        raise SystemExit
