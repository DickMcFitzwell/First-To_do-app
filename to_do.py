import json
import os

def main():
    os.system("cls")
    tasks = load_tasks()
    if not tasks:
        print("No Tasks Yet")
        print("")
    else:
        print("Current Tasks:")
        for task in tasks:
            print(task)
        print("")

    mode = input("Would you like to \"add\", \"complete\", or \"delete\" a task?\n").strip().lower()
    
    if mode == "add":
        n = input("New Task?\n")
        if n:
            if any(t.description.lower() == n.strip().lower() for t in tasks):
                print(f"{n} already exists\n")
                print("")
                return
            else:
                tasks.append(Task(n))
                save_tasks(tasks)
                tasks = load_tasks()
        os.system("cls")
    elif mode == "complete":
        if not tasks:
            print("No tasks to complete\n")
            return
        n = input("Task to mark complete?\n")
        complete_task(n)
        tasks = load_tasks()
    elif mode == "delete":
        if not tasks:
            print("No tasks to delete\n")
            return
        n = input("Task to delete?\n")
        delete_task(n)
        tasks = load_tasks()
    else:
        print("Nothing added or deleted\n")

    if tasks:
        print("Current Tasks:")
        for task in tasks:
            print(task)
        print("")
    else:
        print("No Tasks")
        print("")


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
def load_tasks(filename = "tasks.json"):
    try:
        with open(filename, "r") as file:
            tasklist = file.read().strip()
            if not tasklist:
                return []
            saved_tasks = json.loads(tasklist)
            return [Task.from_dict(x) for x in saved_tasks]
    except FileNotFoundError:
        return []


def save_tasks(tasks, filename = "tasks.json"):
    with open(filename, "w") as file:
        json.dump([task.to_dict() for task in tasks], file, indent = 2)


def delete_task(task, filename = "tasks.json"):
    try:
        with open(filename, "r") as file:
            saved_tasks = json.load(file)
    except FileNotFoundError:
        print("Tasks file not found")
        print("")
        return 
    saved_tasks = [Task.from_dict(d) for d in saved_tasks]
    target_task = next((t for t in saved_tasks if t.description.lower().startswith(task.lower())), None)
    if target_task is None:
        print("Task not found")
        print("")
        return
    else:
        saved_tasks.remove(target_task)
        save_tasks(saved_tasks, filename)
        print(f"{target_task.description} deleted!")
        print("")


def complete_task(task, filename = "tasks.json"):
    try:
        with open(filename, "r") as file:
            saved_tasks = json.load(file)
    except FileNotFoundError:
        print("File not found\n")
        print("")
        return
    saved_tasks = [Task.from_dict(d) for d in saved_tasks]
    found = False
    for t in saved_tasks:
        if t.description.lower().startswith(task.lower()):
            if t.is_complete == True:
                print(f"{t.description} is already completed\n")
                print("")
                return
            t.mark_complete()
            found = True
            break
    if found:
        with open(filename, "w") as file:
            json.dump([t.to_dict() for t in saved_tasks], file, indent=2)
            print(f"{t.description} marked complete\n")
            print("")
    else:
        print("Task not found\n")
        print("")





if __name__ == "__main__":
    main()