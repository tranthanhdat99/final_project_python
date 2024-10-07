import os
import json
from datetime import datetime, timedelta

TASKS_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=2)

def add_task(tasks):
    '''
    Show all task
    task = {
        "id": 
        "title": 
        "category": 
        "description":
        "add_date"
        "due_date": 
        "finished_date": 
        "completed": 
    }
    '''
    # TODO: Fill here
    if not tasks:
        id = 1
    else:
        last_task = tasks[-1]
        id = last_task['id'] + 1
    
    title = input("Enter the title of the new task: ").strip()
    while title == '':
        print('Title can not be empty.')
        title = input("Enter the title of the new task: ").strip()
    
    category = input("Enter the category of the new task: ").strip()
    while category == '':
        print('Category can not be empty.')
        category = input("Enter the category of the new task: ").strip()
    
    description = input("Enter the description of the new task: ")

    today = datetime.now()
    add_date = today.strftime("%Y-%m-%d")

    datetime_format = ['%d-%m-%Y', '%d-%m-%y', '%d/%m/%Y', '%d/%m/%y', '%Y-%m-%d', '%y-%m-%d', '%Y/%m/%d', '%y/%m/%d', '%m-%d-%Y', '%m-%d-%y', '%m/%d/%Y', '%m/%d/%y']
    
    check_date = None
    while True:

        due_date_in = input("Enter the due date of the new task: ").strip()
        
        if due_date_in == '':
            print('Due date can not be empty.')
            continue
        
        for fmat in datetime_format:
            try:
                check_date = datetime.strptime(due_date_in, fmat)
                break
            except ValueError:
                continue
    
        if check_date:
            today = datetime.now()
            if (check_date - today).days < 0:
                print('Due date can not be in the past.')
            else:
                break
        
        else:
            print('Please enter the date with a valid format.')
    
    due_date = check_date.strftime("%Y-%m-%d")

    finished_date = ""

    completed = False

    new_task = {
        "id": id,
        "title": title,
        "category": category,
        "description": description,
        "add_date": add_date,
        "due_date": due_date,
        "finished_date": finished_date,
        "completed": completed
    }

    tasks.append(new_task)

    save_tasks({"tasks": tasks})
    print("Add task successfully.")
    

def list_tasks(tasks):
    '''
    Show all task
    '''
    # TODO: Fill here
    if not tasks:
        print("There's no tasks in the management file.")
        return

    print(f"{'ID':<5} {'Title':<30} {'Category':<15} {'Description':<70} {'Add Date':<15} {'Due Date':<15} {'Finished Date':<15} {'Compeleted':<10}")

    for task in tasks:
        id = task.get('id')
        title = task.get('title')
        category = task.get('category')
        description = task.get('description')
        add_date = task.get("add_date")
        due_date = task.get("due_date")
        finished_date = task.get("finished_date")
        status = task.get("completed")
        
        print(f"{id:<5} {title:<30} {category:<15} {description:<70} {add_date:<15} {due_date:<15} {finished_date:<15} {status:<10}")
    

def mark_task_completed(tasks):
    '''
    Change state of the task to complete and add finish date
    '''
    task_id = int(input("Enter the ID of the task to mark as completed: "))
    # TODO: Fill here
    if not tasks:
        print("There's no tasks in the management file.")
        return
    
    task_found = False

    for task in tasks:
        if task["id"] == task_id:
            task_found =  True
            task["completed"] = True
            print(f"Task ID {task_id} marked as completed.")
            
            today = datetime.now()
            task["finished_date"] = today.strftime("%Y-%m-%d")
            print("Finished date updated.")
            
            break
        
    if task_found == False:
        print(f"Can not find a task with ID {task_id}.")
        return 
    
    save_tasks({"tasks": tasks})


def delete_task(tasks):
    '''
    Delete a task
    '''
    task_id = int(input("Enter the ID of the task to delete: "))
    # TODO: Fill here
    if not tasks:
        print("There's no tasks in the management file.")
        return
    
    task_found = False
    
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            task_found = True
            print(f'Task ID {task_id} has been successfully deleted.')
            
            break
    
    if task_found == False:    
        print(f"Can not find a task with ID {task_id}.")
        return 
    
    save_tasks({"tasks": tasks})


def search_tasks(tasks):
    '''
    Find task by keyword, check the keyword is inside description, title or id 
    '''
    keyword = input("Enter a keyword to search for: ").lower()
    # TODO: Fill here
    target_tasks = []

    if not tasks:
        print("There's no tasks in the management file.")
        return
    
    for task in tasks:
        if keyword in str(task['id']) or keyword in task['title'].lower() or keyword in task['description'].lower():
            target_tasks.append(task)
    
    if target_tasks == []:
        print(f'Can not find any tasks with the keyword "{keyword}"')
        return
    else:
        print(f'List of tasks founded with the keyword "{keyword}":')
        print(f"{'ID':<5} {'Title':<30} {'Category':<15} {'Description':70} {'Add Date':<15} {'Due Date':<15} {'Finished Date':<15} {'Compeleted':<10}")

        for task in target_tasks:
            id = task.get('id')
            title = task.get('title')
            category = task.get('category')
            description = task.get('description')
            add_date = task.get("add_date")
            due_date = task.get("due_date")
            finished_date = task.get("finished_date")
            status = task.get("completed")
        
            print(f"{id:<5} {title:<30} {category:<15} {description:<70} {add_date:<15} {due_date:<15} {finished_date:<15} {status:<10}")
        return