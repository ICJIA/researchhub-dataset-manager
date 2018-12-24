import atexit
import webdatatools as wd

def simplecount_manual_input():
    """Implement business logic for manually updating select data."""
    print('Please place the input data file in the csv format to "input" folder.')
    if wd.ui.prompt_for_confirmation('the input data is ready'):
        temp_created = wd.simplecount.fetch_input_and_create_temp()
        if not temp_created:
            print('ERROR: Cannot create temporary tables!')
            return False
        else:
            if wd.ui.prompt_for_confirmation('the temporary output is as expected'):
                updated = wd.simplecount.finalize_update()
                if not updated:
                    print('ERROR: Cannot finalize the update!')
                    return 'failure'
                else:
                    wd.database.update_output_years()
                    return 'success'

def simplecount_auto_input(source_group_input, source_input):
    """Implement business logic for automatically updating select data."""    
    if source_group_input not in range(2,6+1):
        raise ValueError('ERROR: Invalid source group input!')

    source_dict = {
        (2, 1): 'chri',
        (3, 1): 'idoc',
        (4, 1): 'idjj',
        (5, 1): 'ucr',
        (6, 1): 'jail',
        (6, 2): 'employment',
        (6, 3): 'poverty'
    }
       
    source = source_dict[(int(source_group_input), int(source_input))]
    temp_created = wd.simplecount.fetch_input_and_create_temp(source, auto=True)
    if not temp_created:
        print(f'ERROR: Cannot create temporary tables for {source}!')
        return 'failure'
    else:
        if wd.ui.prompt_for_confirmation('the temporary output is as expected'):
            updated = wd.simplecount.finalize_update(source)
            if not updated:
                print('ERROR: Cannot finalize the update!')
                return 'failure'
            else:
                wd.database.update_output_years()
                return 'success'

def task_simplecount():
    """Implement business logic for updating data for maintained datasets excluding population estimates."""
    wd.database.init()
    wd.simplecount.init()

    simplecount_input = wd.ui.prompt_for_simplecount_input()
    if simplecount_input == 'b':
        return 'back'

    auto = True if simplecount_input == '1' else False
    if auto:
        source_group_input = wd.ui.prompt_for_source_group_input('updating simplecount', auto)
        if source_group_input == 'b':
            return 'back'

        source_input = wd.ui.prompt_for_data_source_input(int(source_group_input))
        if source_input == 'b':
            return 'back'

        return simplecount_auto_input(int(source_group_input), int(source_input))
    else:
        return simplecount_manual_input()    

def task_population():
    """Implement business logic for updating population estimates."""
    wd.database.init()
    wd.population.init()
    
    population_input = wd.ui.prompt_for_population_input()
    if population_input == 'b':
        return 'back'

    auto = False if population_input == '3' else True
    multi = True if population_input == '1' else False
    temp_created = wd.population.fetch_input_and_create_temp(auto, multi)
    
    if not temp_created:
        print('ERROR: Cannot create temporary tables!')
        return 'failure'
    else:
        if wd.ui.prompt_for_confirmation('the temporary output is as expected'):
            updated = wd.population.finalize_update()
            if not updated:
                print('ERROR: Cannot finalize the update!')
                return 'failure'
            else:
                wd.database.update_output_years(pop=True)
                return 'success'

def task_dataset():
    """Implement business logic for generating packaged dataset products."""
    wd.database.init()
    wd.outputtools.init()

    source_group_input = wd.ui.prompt_for_source_group_input('for generating datasets')
    if source_group_input == 'b':
        return 'back'

    package_input = wd.ui.prompt_for_dataset_package_input(int(source_group_input))
    if package_input == 'a':
        print('WAIT: Generating the datasets...')
        generated = wd.outputtools.generate_packages_by_source_group(int(source_group_input))
        print('NOTE: All datasets are generated!')
    elif package_input == 'b':
        return 'back'
    else:
        print('WAIT: Generating the dataset...')
        generated = wd.outputtools.generate_package(int(package_input))
    
    if not generated:
        print('ERROR: Cannot generate dataset packages!')
        return 'failure'
    else:
        return 'success'

@atexit.register
def reset_env(exit=True):
    """Reset the environment by cleaning out all temporary outputs."""
    print('NOTE: Resetting the environment...')
    wd.database.init()
    wd.database.delete_temp()
    wd.outputtools.delete_temp()
    wd.database.close()
    if exit:
        print('NOTE: Exiting the program... Goodbye!\n')

def handle_task_result(result):
    """Receive the task result and take appropriate actions based on the result."""
    while True:
        if result == 'success':
            wd.ui.prompt_for_new_task(success=True)
            reset_env(exit=False)
            break
        elif result == 'failure':
            wd.ui.prompt_for_new_task(success=False)
            reset_env(exit=False)
            break
        elif result == 'back':
            break
    
def main():
    reset_env(exit=False)
    welcome_msg = '\n### WELCOME TO ICJIA WEB DATASET MAINTENANCE TOOL ###' +\
        '\n\nYou can safely exit this program by typing "q" and press Enter' +\
        ' whenever asked for your input.' +\
        '\n***WARNING: Trying to forcibly quit the program might cause' +\
        ' unexpected problems.***' +\
        '\n'
    print(welcome_msg)
    while True:
        task_code = wd.ui.prompt_for_task_input()
        if task_code == '1':
            handle_task_result(task_simplecount())
        elif task_code == '2':
            handle_task_result(task_population())
        elif task_code == '3':
            handle_task_result(task_dataset())

if __name__ == '__main__':
    main()