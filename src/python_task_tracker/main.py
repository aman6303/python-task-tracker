import argparse

from python_task_tracker.config import PRIORITIES
from python_task_tracker.database import init_db
from python_task_tracker.services import create_task, complete_task, list_task, remove_task

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

            if not tasks:
                print("No task found!\n")
            else:
                print(f"\n{'ID':<5} {'Status':<8} {'Priority':<10} {'Due':<12} {'Title':<20} Description")
                print("-" * 70)

                for t in tasks:
                    due = t.due_date or "-" # replacing empty value in due with -
                    description = t.description or "-"
        
                    print(f"{t.id:<5} {t.status:<8} {t.priority:<10} {due:<12} {t.title:<20} {description}")


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
def main()-> None:
    init_db()

    
    interactive_menu()

if __name__ == "__main__":
    main()