import argparse

from python_task_tracker.config import PRIORITIES
from python_task_tracker.database import init_db
from python_task_tracker.services import create_task, complete_task, list_task, remove_task

# helper function to print tasks in tabular format
def print_tasks(tasks: list) -> None:
    if not tasks:
        print("No task found!\n")
    else:
        print(f"\n{'ID':<5} {'Status':<8} {'Priority':<10} {'Due':<12} {'Title':<20} Description")
        print("-" * 70)
        for t in tasks:
            due = t.due_date or "-"
            description = t.description or "-"
            print(f"{t.id:<5} {t.status:<8} {t.priority:<10} {due:<12} {t.title:<20} {description}")
        print()


# code for interactive mode
def interactive_menu() -> None:
    print(f"\n{'-----PERSONAL TASK TRACKER-----':^40}")
    print("Interactive mode (type a number or enter 'q' to quit)\n")

    while True:
        print("1. Add task")
        print("2. List tasks")
        print("3. Mark task done")
        print("4. Delete task")
        print("q. quit")
        choice = input("\nChoose an option: ").strip().lower()

        if choice == "1":

            while True:
                title = input("Enter task title (in less than 20 letters): ").strip()
                if not title:
                    print("Title cannot be empty.\n")
                    continue
                if len(title) > 20:
                    print("Title cannot have more than 20 letters.\n")
                    continue
                break  # Valid title entered, exit the inner loop

            priority = input("Priority (low/medium/high, default medium): ").strip().lower() or "medium"
            if priority not in PRIORITIES:
                priority = "medium"

            due = input("Due date YYYY-MM-DD (optional): ").strip() or None

            # we can verify input date here but i am leaving it here
            desc = input("Description (optional): ").strip()
            t = create_task(title, priority, due, desc)

            print(f"Created task '{t.title}' (ID: {t.id})\n")
        elif choice == "2":
            status = input("Filter by status(todo/done/all, default all): ").strip().lower() or None
            if status == "all":
                status = None
            tasks = list_task(status)
            print_tasks(tasks)


        elif choice == "3":
            try:
                tid = int(input("Enter task ID to mark it done: ").strip())
                if complete_task(tid):
                    print("Task marked as done.\n")
                else:
                    print("Task not found!\n")
            except ValueError:
                print("Invalid ID.\n")

        elif choice == "4":
            try:
                tid = int(input("Enter task ID to delete: ").strip())
                if remove_task(tid):
                    print("Task deleted.\n")
                else:
                    print("Task not found!\n")
            except ValueError:
                print("Invalid ID.\n")

        elif choice in ("q", "quit", "exit"):
            print("thanks for using the program!!!")
            break
        else:
            print("Invalid Option!!!\n")
        

# contain feature of interactive cli as well as direct cli
def main() -> None:
    init_db()

    parser = argparse.ArgumentParser(description="Personal Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title (less than 20 characters)")
    add_parser.add_argument(
        "--priority", "-p",
        choices=PRIORITIES,
        default="medium",
        help="Task priority (low, medium, high; default: medium)"
    )
    add_parser.add_argument("--due", "-d", help="Due date YYYY-MM-DD (optional)")
    add_parser.add_argument("--desc", default="", help="Description (optional)")

    # list command
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument(
        "--status", "-s",
        choices=["todo", "done", "all"],
        default="all",
        help="Filter by status (todo, done, all; default: all)"
    )

    # done command
    done_parser = subparsers.add_parser("done", help="Mark a task as done")
    done_parser.add_argument("id", type=int, help="Task ID to mark done")

    # delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID to delete")

    args = parser.parse_args()

    # Default to interactive mode if no command is specified
    if args.command is None:
        interactive_menu()
        return

    # Direct command execution
    if args.command == "add":
        if len(args.title) > 20:
            print("Error: Title cannot have more than 20 letters.\n")
            return
        t = create_task(args.title, args.priority, args.due, args.desc)
        print(f"Created task '{t.title}' (ID: {t.id})\n")

    elif args.command == "list":
        status = None if args.status == "all" else args.status
        tasks = list_task(status)
        print_tasks(tasks)

    elif args.command == "done":
        if complete_task(args.id):
            print(f"Task {args.id} marked as done.\n")
        else:
            print(f"Task {args.id} not found!\n")

    elif args.command == "delete":
        if remove_task(args.id):
            print(f"Task {args.id} deleted.\n")
        else:
            print(f"Task {args.id} not found!\n")


if __name__ == "__main__":
    main()
