import argparse
from python_task_tracker.config import PRIORITIES

# code for interactive mode
def interactive_menu() -> None:
    print("\n=== Personal task Tracker ===")
    print("\nInteractive mode (type a number or enter 'q' to quit)\n")

    while True:
        print("1. Add task")
        print("2. List tasks")
        print("3. Mark task done")
        print("4. Delete task")
        print("q. quit")
        choice = input("\nChoose an option: ").strip().lower()

        if choice == "1":
            title = input("Enter task title: ").strip()
            if not title:
                print("Title cannot be empty.\n")
                continue
            priority = input("Priority (low/medium/high, default medium): ").strip().lower() or "medium"
            if priority not in PRIORITIES:
                priority = "medium"
            due = input("Due date YYYY-MM-DD (optional): ").strip() or None
            # we can verify input date here but i am leaving it here
            desc = input("Description (optional): ").strip
            t = create_task(title, priority, due, desc)
            print(f"Created task '{t.title}' (ID: {t.id})\n")

        elif choice in ("q", "quit", "exit"):
            print("thanks for using the program!!!")
            break
        else:
            print("Invalid Option!!!\n")
        

def main()-> None:
    interactive_menu()

if __name__ == "__main__":
    main()