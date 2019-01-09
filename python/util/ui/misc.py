from time import sleep

def prompt_user(msg, errmsg, isvalid):
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

def complete_choices(msg, range_choice, prompt, all=False, back=True):
    """Return the complete message and choice list.""" 
    list_choice = [str(i) for i in range_choice]
    
    if all:
        list_choice += ['a']
        msg += '\n- a - All of the above.'

    if back:
        list_choice += ['b']
        msg += '\n- b - Back to the main menu.'
    
    list_choice += ['q']
    msg += f'\n- q - Exit the program.\n\n> {prompt}? [{"/".join(list_choice)}]'

    return msg, list_choice

def handle_exit():
    msg = '\nAre you sure you wish to exit the program?' +\
        ' All intermediary results will be abandoned.' +\
        '\n\n> Exit? [y/n]'
    errmsg = 'ERROR: Invalid response! Try again.'
    isvalid = lambda x: x in ['y', 'n']
    
    exit_input = prompt_user(msg, errmsg, isvalid)
    if exit_input == 'y':
        raise SystemExit
    else:
        pass