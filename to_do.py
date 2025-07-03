import json

def main():
    tasks = load_tasks()
    if not tasks:
        print("No Tasks Yet")
        print("")
    else:
        print("Current Tasks:")
        for task in tasks:
            print(task)
        print("")

    n = input("New Task?\n")
    tasks.append(Task(n))
    save_tasks(tasks)

    if tasks:
        print("Current Tasks:")
        for task in tasks:
            print(task)
    else:
        print("No Tasks")


# define classes
class Task:
    def __init__ (self, description, is_complete = False):
        self.description = description
        self.is_complete = is_complete

    def __str__(self):
        status = "Completed" if self.is_complete else "Incomplete"
        return f"{self.description} [{status}]"

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
            saved_tasks = json.load(file)
            return [Task.from_dict(x) for x in saved_tasks]
    except FileNotFoundError:
        return []


def save_tasks(tasks, filename = "tasks.json"):
    with open(filename, "w") as file:
        json.dump([task.to_dict() for task in tasks], file, indent = 2)



if __name__ == "__main__":
    main()