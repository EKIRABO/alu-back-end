#!/usr/bin/env python3
"""
Script to display employee TODO list progress from a REST API.
"""

import sys
import urllib.request
import json


def get_employee_todo_progress(employee_id):
    """
    Fetches and displays TODO list progress for a given employee ID.
    
    Args:
        employee_id (int): The employee ID
    """
    
    try:
        # Fetch employee data
        employee_url = f"https://jsonplaceholder.typicode.com/users/{employee_id}"
        with urllib.request.urlopen(employee_url) as response:
            employee_data = json.loads(response.read().decode())
        
        employee_name = employee_data.get("name", "Unknown")
        
        # Fetch todos for this employee
        todos_url = f"https://jsonplaceholder.typicode.com/users/{employee_id}/todos"
        with urllib.request.urlopen(todos_url) as response:
            todos_data = json.loads(response.read().decode())
        
        # Count completed and total tasks
        completed_tasks = [todo for todo in todos_data if todo.get("completed")]
        total_tasks = len(todos_data)
        completed_count = len(completed_tasks)
        
        # Display first line with progress
        print(f"Employee {employee_name} is done with tasks({completed_count}/{total_tasks}):")
        
        # Display completed task titles
        for task in completed_tasks:
            print(f"\t {task.get('title', 'Untitled')}")
    
    except urllib.error.HTTPError as e:
        print(f"Error: Employee ID {employee_id} not found (HTTP {e.code})", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <employee_id>", file=sys.stderr)
        sys.exit(1)
    
    try:
        employee_id = int(sys.argv[1])
    except ValueError:
        print("Error: Employee ID must be an integer", file=sys.stderr)
        sys.exit(1)
    
    get_employee_todo_progress(employee_id)
