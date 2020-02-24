from database.main import drop_temp, update_dataset_years
from fs.main import delete_input, delete_temp, write_dataset, write_datasets_in_group
from ui.io import create_temp_data, create_temp_bridgepop, update_data, update_bridgepop
from ui.prompt import (prompt_for_confirmation, prompt_for_data_input,
    prompt_for_data_source_input, prompt_for_dataset_input, prompt_for_new_task,
    prompt_for_population_input, prompt_for_group_input)

def __data_manual_input():
    """Implement business logic for manually updating select data."""
    print('Please place the input data file in the csv format to "input" folder.')
    if prompt_for_confirmation('the input data is ready'):
        
        temp_created = create_temp_data()

        if not temp_created:
            print("ERROR: Cannot create temporary tables!")
            return False
        else:
            delete_input()
            if prompt_for_confirmation("the temporary output is as expected"):
                updated = update_data()
                if not updated:
                    print("ERROR: Cannot finalize the update!")
                    return 'failure'
                else:
                    update_dataset_years()
                    return 'success'

def __data_auto_input(group_input, source_input):
    """Implement business logic for automatically updating select data."""    
    if group_input not in range(2,6+1):
        raise ValueError("ERROR: Invalid group input!")

    source_dict = {
        (2, 1): 'chri',
        (3, 1): 'idoc',
        (4, 1): 'idjj',
        (5, 1): 'ucr',
        (6, 1): 'jail',
        (6, 2): 'employment',
        (6, 3): 'poverty'
    }
       
    source = source_dict[(int(group_input), int(source_input))]
    temp_created = create_temp_data(source, auto=True)
    if not temp_created:
        print(f"ERROR: Cannot create temporary tables for {source}!")
        return 'failure'
    else:
        if prompt_for_confirmation("the temporary output is as expected"):
            updated = update_data(source)
            if not updated:
                print("ERROR: Cannot finalize the update!")
                return 'failure'
            else:
                update_dataset_years()
                return 'success'

def reset_env(exit=True):
    """Reset the environment by cleaning out all temporary outputs."""
    print("NOTE: Resetting the environment...")
    
    drop_temp()
    delete_temp()
    
    if exit:
        print("NOTE: Exiting the program... Goodbye!\n")

def task_data():
    """Implement business logic for updating data for maintained datasets excluding population estimates."""
    data_input = prompt_for_data_input()
    if data_input == 'b':
        return 'back'

    auto = True if data_input == '1' else False
    if auto:
        group_input = prompt_for_group_input("updating data", auto)
        if group_input == 'b':
            return 'back'

        source_input = prompt_for_data_source_input(int(group_input))
        if source_input == 'b':
            return 'back'

        return __data_auto_input(int(group_input), int(source_input))
    else:
        return __data_manual_input()    

def task_population():
    """Implement business logic for updating population estimates."""
    population_input = prompt_for_population_input()
    if population_input == 'b':
        return 'back'

    temp_created = create_temp_bridgepop()
    
    if not temp_created:
        print("ERROR: Cannot create temporary tables!")
        return 'failure'
    else:
        if prompt_for_confirmation("the temporary output is as expected"):
            updated = update_bridgepop()
            if not updated:
                print("ERROR: Cannot finalize the update!")
                return 'failure'
            else:
                update_dataset_years(pop=True)
                return 'success'

def task_dataset():
    """Implement business logic for generating packaged dataset products."""
    group_input = prompt_for_group_input("for generating datasets")
    if group_input == 'b':
        return 'back'

    dataset_input = prompt_for_dataset_input(int(group_input))
    if dataset_input == 'a':
        print("WAIT: Generating the datasets...")
        generated = write_datasets_in_group(int(group_input))
        print("NOTE: All datasets are generated!")
    elif dataset_input == 'b':
        return 'back'
    else:
        print("WAIT: Generating the dataset...")
        generated = write_dataset(int(dataset_input))
    
    if not generated:
        print("ERROR: Cannot generate dataset packages!")
        return 'failure'
    else:
        return 'success'

def handle_task_result(result):
    """Receive the task result and take appropriate actions based on the result."""
    while True:
        if result == 'success':
            prompt_for_new_task(success=True)
            reset_env(exit=False)
            break
        elif result == 'failure':
            prompt_for_new_task(success=False)
            reset_env(exit=False)
            break
        elif result == 'back':
            break