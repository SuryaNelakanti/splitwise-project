# Splitwise App

The Splitwise App is a simple expense tracking and splitting application that helps users manage shared expenses among friends, roommates, or groups. It allows users to create groups, add expenses, and keep track of who owes whom.

Features
User Registration: Users can register in the app

Create Groups: Users can create groups and invite other users to join the group.

Add Expenses: Users can add expenses with details such as the amount, description, and participants involved.

Split Expenses: The app automatically calculates and tracks the amount owed by each user within a group.

View Balances: Users can view their balances and see how much they owe or are owed by other group members.

Technologies Used
Backend: FastAPI (Python), SQLAlchemy (Python), PostgreSQL (Database)

Getting Started
To run the App locally, follow these steps:

Clone the repository:

```bash
git clone <repository-url>
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Set up the database:
Create a PostgreSQL database.
Update the database connection details in the alembic.ini file.
Run database migrations:

```bash
alembic upgrade head
```

Start the backend server:

```bash
uvicorn main:app --reload
```

OR

Build the Docker image using the Dockerfile:

```bash
docker build -t my-app-image .
```

Run the Docker Compose file:

```bash
docker-compose up
```
