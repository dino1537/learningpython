import os
import csv
import json
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from datetime import datetime

# Define the SQLAlchemy database setup
DATABASE_URL = "sqlite:///tasks.db"
# Allow users to customize the database URL through an environment variable
if "TASK_MANAGER_DB_URL" in os.environ:
    DATABASE_URL = os.environ["TASK_MANAGER_DB_URL"]

engine = create_engine(DATABASE_URL)
Base = declarative_base()


# Define the Task model with priority field
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    priority = Column(Enum("low", "medium", "high"), default="low")


# Create the database tables
Base.metadata.create_all(bind=engine)

# Create a Session to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def add_task(title, description, priority):
    session = SessionLocal()
    task = Task(title=title, description=description, priority=priority)
    session.add(task)
    session.commit()
    session.close()


def update_task(task_id, title, description, completed, priority):
    session = SessionLocal()
    task = session.query(Task).filter(Task.id == task_id).first()

    if task:
        task.title = title
        task.description = description
        task.completed = completed
        task.priority = priority
        session.commit()
    else:
        print("Task not found.")

    session.close()


def delete_task(task_id):
    session = SessionLocal()
    task = session.query(Task).filter(Task.id == task_id).first()

    if task:
        session.delete(task)
        session.commit()
        print("Task deleted successfully.")
    else:
        print("Task not found.")

    session.close()


def list_tasks(page=1, page_size=5, sort_by_priority=False):
    session = SessionLocal()

    if sort_by_priority:
        tasks = (
            session.query(Task)
            .order_by(Task.priority, Task.created_at)
            .limit(page_size)
            .offset((page - 1) * page_size)
            .all()
        )
    else:
        tasks = (
            session.query(Task)
            .order_by(Task.created_at)
            .limit(page_size)
            .offset((page - 1) * page_size)
            .all()
        )

    if not tasks:
        print("No tasks found.")
    else:
        for task in tasks:
            print(f"Task ID: {task.id}")
            print(f"Title: {task.title}")
            print(f"Description: {task.description}")
            print(f"Completed: {'Yes' if task.completed else 'No'}")
            print(f"Priority: {task.priority}")
            print(f"Created At: {task.created_at}")
            print("-" * 40)

    session.close()


def export_tasks_to_csv(filename):
    session = SessionLocal()
    tasks = session.query(Task).all()

    if tasks:
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["ID", "Title", "Description", "Completed", "Priority", "Created At"]
            )
            for task in tasks:
                writer.writerow(
                    [
                        task.id,
                        task.title,
                        task.description,
                        task.completed,
                        task.priority,
                        task.created_at,
                    ]
                )
        print(f"Tasks exported to {filename} successfully.")
    else:
        print("No tasks found to export.")

    session.close()


def export_tasks_to_json(filename):
    session = SessionLocal()
    tasks = session.query(Task).all()

    if tasks:
        task_list = []
        for task in tasks:
            task_list.append(
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "priority": task.priority,
                    "created_at": task.created_at.isoformat(),
                }
            )
        with open(filename, "w") as file:
            json.dump(task_list, file, indent=4)
        print(f"Tasks exported to {filename} successfully.")
    else:
        print("No tasks found to export.")

    session.close()


if __name__ == "__main__":
    while True:
        print("\nTask Manager")
        print("1. Add Task")
        print("2. Update Task")
        print("3. Delete Task")
        print("4. List Tasks")
        print("5. Export Tasks to CSV")
        print("6. Export Tasks to JSON")
        print("7. Quit")

        choice = input("Select an option (1/2/3/4/5/6/7): ")

        if choice == "1":
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            priority = input("Enter task priority (low/medium/high): ").lower()
            add_task(title, description, priority)
            print("Task added successfully!")
        elif choice == "2":
            task_id = int(input("Enter task ID to update: "))
            title = input("Enter new task title: ")
            description = input("Enter new task description: ")
            completed = input("Is the task completed? (yes/no): ").lower() == "yes"
            priority = input("Enter task priority (low/medium/high): ").lower()
            update_task(task_id, title, description, completed, priority)
            print("Task updated successfully!")
        elif choice == "3":
            task_id = int(input("Enter task ID to delete: "))
            delete_task(task_id)
        elif choice == "4":
            page = int(input("Enter page number: "))
            sort_by_priority = input("Sort by priority? (yes/no): ").lower() == "yes"
            list_tasks(page, sort_by_priority=sort_by_priority)
        elif choice == "5":
            filename = input("Enter CSV file name to export tasks: ")
            export_tasks_to_csv(filename)
        elif choice == "6":
            filename = input("Enter JSON file name to export tasks: ")
            export_tasks_to_json(filename)
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")
