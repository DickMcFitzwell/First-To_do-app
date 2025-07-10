import json
import os

def main():
    os.system("cls")
    filename = choose_list()
    tasks = app_start(filename)
    editing = True
    while editing == True:
        mode = input("Would you like to \"add\", \"complete\", \"delete\" a task or \"change\" list or \"exit\"?\n").strip().lower()
        
        if mode == "add":
            tasks = add_task(tasks, filename)
        elif mode == "complete":
            tasks = complete_task(tasks, filename)
        elif mode == "change":
            filename = choose_list()
            tasks = load_tasks(filename)
        elif mode == "delete":
            tasks = delete_task(tasks, filename)
        elif mode == "exit":
            editing = False
        else:
            print("Nothing added or deleted\n")
        if tasks:
            print("Current Tasks:")
            for task in tasks:
                print(task)
            print("")
        else:
            print("No Tasks\n")



# define classes
class Task:
    def __init__ (self, description, is_complete = False):
        self.description = description.capitalize()
        self.is_complete = is_complete

    def __str__(self):
        status = "Completed" if self.is_complete else "Incomplete"
        return f"[{status}] {self.description}"

    def mark_complete(self):
        self.is_complete = True

    def to_dict(self):
        return{
            "description" : self.description,
            "is_complete" : self.is_complete
        }
    
    @staticmethod
    def from_dict(dict):
        return Task(dict["description"], dict["is_complete"])


# define functions

def add_task(tasks, filename):
    n = input("New Task?\n")
    if not n:
        return tasks
    if any(t.description.lower() == n.strip().lower() for t in tasks):
        print(f"{n.strip().capitalize()} already exists\n")
        return tasks
    else:
        tasks.append(Task(n))
        save_tasks(tasks, filename)
        os.system("cls")
    return tasks


def app_start(filename):
    os.system("cls")
    tasks = load_tasks(filename)
    if not tasks:
        print("No Tasks Yet\n")
    else:
        print("Current Tasks:")
        for task in tasks:
            print(task)
        print("")  
    return tasks  


def choose_list():
    lists = [f[:-5] for f in os.listdir() if f.lower().endswith(".json")]
    print("Current lists:")
    print(lists or "No active lists\n")
    choice = input("Would you like to \"open\", \"create\", or \"delete\" a list?\n").strip().lower()
    if choice == "create":
        name = input("Name your new list:\n").strip().lower()
        if name in lists:
            print(f"{name} already exists!")
        else:
            with open(f"{name}.json", "w") as filename:
                json.dump([], filename)
        return choose_list()
    elif choice == "open":
        if not lists:
            print("No list to open\n")
            return choose_list()
        name = input("Which list would you like to open?\n").strip().lower()
        if not name in lists:
            print(f"{name} not found!\n")
            return choose_list()
        else:
            return f"{name}.json"
    elif choice == "delete":
        if not lists:
            print("No list to delete\n")
            return choose_list()
        name = input("Which list would you like to delete?\n").strip().lower()
        if os.path.exists(f"{name}.json"):
            os.remove(f"{name}.json")
            print(f"{name} has been deleted!\n")
        else:
            print(f"{name} not found!\n")
        return choose_list()
    else:
        print("Invalid option\n")
        return choose_list()


def complete_task(tasks, filename):
    if not tasks:
        print("No tasks to complete\n")
        return tasks
    task = input("Task to mark complete?\n")
    found = False
    for t in tasks:
        if t.description.lower().startswith(task.lower()):
            if t.is_complete:
                print(f"{t.description} is already completed\n")
            else:
                t.mark_complete()
                save_tasks(tasks, filename)
                print(f"{t.description} marked complete\n")
            found = True
            break
    if not found:
        print("Task not found\n")
    return tasks


def delete_task(tasks, filename):
    if not tasks:
        print("No tasks to delete\n")
        return tasks
    task = input("Task to delete?\n")
    target_task = next((t for t in tasks if t.description.lower().startswith(task.lower())), None)
    if target_task is None:
        print("Task not found\n")
        return tasks
    else:
        tasks.remove(target_task)
        save_tasks(tasks, filename)
        print(f"{target_task.description} deleted!\n")
    return tasks


def load_tasks(filename):
    try:
        with open(filename, "r") as file:
            tasks = file.read().strip()
            if not tasks:
                return []
            tasks = json.loads(tasks)
            return [Task.from_dict(x) for x in tasks]
    except FileNotFoundError:
        return []


def save_tasks(tasks, filename):
    with open(filename, "w") as file:
        json.dump([task.to_dict() for task in tasks], file, indent = 2)



if __name__ == "__main__":
    main()