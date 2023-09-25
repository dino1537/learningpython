import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
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

# Define the Task model
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Create a Session to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def add_task(title, description):
    session = SessionLocal()
    task = Task(title=title, description=description)
    session.add(task)
    session.commit()
    session.close()

def update_task(task_id, title, description, completed):
    session = SessionLocal()
    task = session.query(Task).filter(Task.id == task_id).first()
    
    if task:
        task.title = title
        task.description = description
        task.completed = completed
        session.commit()
    else:
        print("Task not found.")
    
    session.close()

def list_tasks(page=1, page_size=5):
    session = SessionLocal()
    tasks = session.query(Task).limit(page_size).offset((page - 1) * page_size).all()
    
    if not tasks:
        print("No tasks found.")
    else:
        for task in tasks:
            print(f"Task ID: {task.id}")
            print(f"Title: {task.title}")
            print(f"Description: {task.description}")
            print(f"Completed: {'Yes' if task.completed else 'No'}")
            print(f"Created At: {task.created_at}")
            print("-" * 40)
    
    session.close()

if __name__ == "__main__":
    while True:
        print("\nTask Manager")
        print("1. Add Task")
        print("2. Update Task")
        print("3. List Tasks")
        print("4. Quit")
        
        choice = input("Select an option (1/2/3/4): ")
        
        if choice == "1":
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            add_task(title, description)
            print("Task added successfully!")
        elif choice == "2":
            task_id = int(input("Enter task ID to update: "))
            title = input("Enter new task title: ")
            description = input("Enter new task description: ")
            completed = input("Is the task completed? (yes/no): ").lower() == "yes"
            update_task(task_id, title, description, completed)
            print("Task updated successfully!")
        elif choice == "3":
            page = int(input("Enter page number: "))
            list_tasks(page)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")
