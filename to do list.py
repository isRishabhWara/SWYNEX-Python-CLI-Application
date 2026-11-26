import json
import os


class ToDoList:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()
        if not os.path.exists(self.filename):
            self.save_tasks()

    def load_tasks(self):
        """Load tasks from the JSON file."""
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(f"Error: '{self.filename}' is corrupted. Starting with an empty list.")
            return []

    def save_tasks(self):
        """Save tasks to the JSON file."""
        with open(self.filename, 'w') as file:
            json.dump(self.tasks, file, indent=4)

    def view_tasks(self):
        """Display all tasks."""
        if not self.tasks:
            print("No tasks to display.")
            return
        for i, task in enumerate(self.tasks, start=1):
            status = "[X]" if task["done"] else "[ ]"
            print(f"{i}. {task['task']} - {status}")

    def add_task(self, task_description):
        """Add a new task and save."""
        self.tasks.append({"task": task_description, "done": False})
        self.save_tasks()
        print(f'Task "{task_description}" added to {self.filename}.')

    def mark_task_done(self, task_number):
        """Mark a task as done by its 1-based index."""
        if 1 <= task_number <= len(self.tasks):
            self.tasks[task_number - 1]["done"] = True
            self.save_tasks()
            print(f'Task "{self.tasks[task_number - 1]["task"]}" marked as done.')
        else:
            print("Invalid task number.")

    def remove_task(self, task_number):
        """Remove a task by its 1-based index."""
        if 1 <= task_number <= len(self.tasks):
            removed = self.tasks.pop(task_number - 1)
            self.save_tasks()
            print(f'Task "{removed["task"]}" removed.')
        else:
            print("Invalid task number.")


def get_lists():
    """Return a sorted list of all JSON list files in the current directory."""
    return sorted(
        f for f in os.listdir('.')
        if os.path.isfile(f) and f.lower().endswith('.json')
    )


def view_lists(current_todo, show_tasks=False):
    """Display all saved lists, optionally showing tasks underneath each list."""
    json_files = get_lists()
    print("\nAvailable lists:")
    if not json_files:
        print("No saved lists found yet.")
        return json_files

    for i, fname in enumerate(json_files, start=1):
        marker = " (current)" if fname == current_todo.filename else ""
        print(f"\n{i}. {fname}{marker}")
        if show_tasks:
            temp_list = ToDoList(fname)
            if not temp_list.tasks:
                print("   (No tasks)")
            else:
                for j, task in enumerate(temp_list.tasks, start=1):
                    status = "[X]" if task["done"] else "[ ]"
                    print(f"   {j}. {task['task']} - {status}")
    return json_files


def browse_and_open_list(current_todo):
    """Show all lists with their tasks and let the user open one to manage it."""
    json_files = view_lists(current_todo, show_tasks=True)
    if not json_files:
        return current_todo

    selection = input("\nEnter a list number to open and manage (or press Enter to go back): ").strip()
    if not selection:
        return current_todo

    if selection.isdigit():
        index = int(selection)
        if 1 <= index <= len(json_files):
            selected_file = json_files[index - 1]
            print(f"Opened '{selected_file}'.")
            return ToDoList(selected_file)

    print("Invalid list number.")
    return current_todo


def switch_list(current_todo):
    """Let the user pick an existing JSON list or create a new one."""
    json_files = view_lists(current_todo, show_tasks=False)

    selection = input("\nEnter a list number, or type a new list name (e.g., shopping): ").strip()
    if not selection:
        return current_todo

    if selection.isdigit():
        index = int(selection)
        if 1 <= index <= len(json_files):
            new_file = json_files[index - 1]
            print(f"Switched to '{new_file}'.")
            return ToDoList(new_file)
        print("Invalid list number.")
        return current_todo

    new_file = selection if selection.lower().endswith('.json') else f"{selection}.json"
    new_todo = ToDoList(new_file)
    print(f"Switched to '{new_file}'.")
    return new_todo


def delete_list(current_todo):
    """Delete an existing JSON list file."""
    json_files = view_lists(current_todo, show_tasks=False)
    if not json_files:
        return current_todo

    selection = input("\nEnter the list number to delete (or press Enter to cancel): ").strip()
    if not selection:
        return current_todo

    try:
        index = int(selection)
        if not (1 <= index <= len(json_files)):
            print("Invalid list number.")
            return current_todo
    except ValueError:
        print("Please enter a valid number.")
        return current_todo

    target_file = json_files[index - 1]
    confirm = input(f"Are you sure you want to delete '{target_file}'? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Deletion cancelled.")
        return current_todo

    os.remove(target_file)
    print(f"List '{target_file}' deleted.")

    if target_file == current_todo.filename:
        remaining = get_lists()
        next_file = remaining[0] if remaining else "tasks.json"
        print(f"Switched to '{next_file}'.")
        return ToDoList(next_file)

    return current_todo


def main():
    todo = ToDoList("tasks.json")

    while True:
        print(f"\nTo-Do List Menu [{todo.filename}]:")
        print("1. View tasks")
        print("2. Add a task")
        print("3. Mark a task as done")
        print("4. Remove a task")
        print("5. View all lists")
        print("6. Switch / Create list")
        print("7. Delete a list")
        print("8. Exit")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            todo.view_tasks()
            if todo.tasks:
                action = input("\nEnter a task number to remove (or press Enter to go back): ").strip()
                if action:
                    try:
                        todo.remove_task(int(action))
                    except ValueError:
                        print("Please enter a valid number.")

        elif choice == '2':
            task_description = input("Enter the task description: ").strip()
            if task_description:
                todo.add_task(task_description)
            else:
                print("Task description cannot be empty.")

        elif choice == '3':
            if not todo.tasks:
                print("No tasks to mark as done.")
                continue
            todo.view_tasks()
            try:
                task_number = int(input("Enter the task number to mark as done: "))
                todo.mark_task_done(task_number)
            except ValueError:
                print("Please enter a valid number.")

        elif choice == '4':
            if not todo.tasks:
                print("No tasks to remove.")
                continue
            todo.view_tasks()
            try:
                task_number = int(input("Enter the task number to remove: "))
                todo.remove_task(task_number)
            except ValueError:
                print("Please enter a valid number.")

        elif choice == '5':
            todo = browse_and_open_list(todo)

        elif choice == '6':
            todo = switch_list(todo)

        elif choice == '7':
            todo = delete_list(todo)

        elif choice == '8':
            todo.save_tasks()
            print("Exiting the to-do list application.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
