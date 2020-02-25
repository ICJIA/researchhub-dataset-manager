import atexit
from ui import (handle_task_result, prompt_for_task_input, reset_env,
    task_data, task_dataset, task_population)

reset_env = atexit.register(reset_env)

def main():
    reset_env(exit=False)
    
    welcome_msg = "\n### WELCOME TO ICJIA RESEARCH HUB DATASET MANAGER ###" +\
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

if __name__ == '__main__':
    main()