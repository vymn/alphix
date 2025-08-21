#!/usr/bin/env python3
"""
Example scripts for testing CLI Hub functionality
"""

import time
import sys
import random
from datetime import datetime


def counter_script():
    """A simple counter that runs indefinitely"""
    count = 0
    while True:
        print(f"Count: {count} - {datetime.now()}")
        count += 1
        time.sleep(2)


def log_generator():
    """Generates random log messages"""
    log_levels = ["INFO", "DEBUG", "WARNING", "ERROR"]
    messages = [
        "Processing request",
        "Database connection established",
        "User login attempt",
        "Cache updated",
        "Backup completed",
        "Service health check",
        "API call received",
    ]

    while True:
        level = random.choice(log_levels)
        message = random.choice(messages)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        time.sleep(random.uniform(1, 3))


def simple_server():
    """Simulates a simple server"""
    print("Starting server on port 8080...")
    print("Server initialized successfully")

    count = 0
    while True:
        count += 1
        print(f"[{datetime.now()}] Request #{count} processed")
        time.sleep(random.uniform(0.5, 2))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python examples.py <script_name>")
        print("Available scripts: counter, logger, server")
        sys.exit(1)

    script_name = sys.argv[1]

    if script_name == "counter":
        counter_script()
    elif script_name == "logger":
        log_generator()
    elif script_name == "server":
        simple_server()
    else:
        print(f"Unknown script: {script_name}")
        sys.exit(1)
