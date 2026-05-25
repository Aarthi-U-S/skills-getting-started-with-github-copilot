"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}

SUPPORTED_OPERATIONS = {"add", "subtract", "multiply", "divide"}


def _validate_int(value: int, field_name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{field_name} must be an integer")


def calculate(num1: int, num2: int, operation: str) -> int:
    """Perform a basic calculator operation on two integers."""
    _validate_int(num1, "num1")
    _validate_int(num2, "num2")

    if not isinstance(operation, str) or not operation.strip():
        raise ValueError("operation is required")

    normalized_operation = operation.strip().lower()
    if normalized_operation not in SUPPORTED_OPERATIONS:
        raise ValueError(
            f"Unsupported operation. Choose one of: {', '.join(sorted(SUPPORTED_OPERATIONS))}"
        )

    if normalized_operation == "add":
        return num1 + num2
    if normalized_operation == "subtract":
        return num1 - num2
    if normalized_operation == "multiply":
        return num1 * num2
    if normalized_operation == "divide":
        if num2 == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return num1 // num2


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.get("/calculator")
def calculator(num1: int, num2: int, operation: str):
    """Calculate a result for two integers using a basic operation."""
    try:
        result = calculate(num1=num1, num2=num2, operation=operation)
        return {
            "num1": num1,
            "num2": num2,
            "operation": operation.strip().lower(),
            "result": result,
        }
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
