# test_debug_vars.py
# Demonstrates how to use the debug variable storage functions

# Add the src directory to the Python path
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import the debug variable functions
from kybra_simple_logging import save_var, load_var, list_vars, logger

# Configure logger to show debug messages
from kybra_simple_logging import set_log_level
set_log_level("DEBUG")

# PART 1: Saving simple variables
print("\n=== Saving and Loading Simple Variables ===\n")
save_var("message", "Hello from debug storage!")
save_var("counter", 42)
save_var("enabled", True)

# PART 2: Retrieving stored variables
print("\n=== Retrieving Stored Variables ===\n")
message = load_var("message")
counter = load_var("counter")
enabled = load_var("enabled")

print(f"Retrieved 'message': {message}")
print(f"Retrieved 'counter': {counter}")
print(f"Retrieved 'enabled': {enabled}")

# PART 3: Retrieving non-existent variables (returns None)
print("\n=== Retrieving Non-existent Variables ===\n")
missing_var = load_var("does_not_exist")
print(f"Retrieved 'does_not_exist': {missing_var}")

# PART 4: Storing complex data types
print("\n=== Storing Complex Data Types ===\n")
user_profile = {
    "name": "Test User",
    "email": "user@example.com",
    "preferences": {
        "theme": "dark",
        "notifications": True
    },
    "history": [1, 2, 3, 4, 5]
}
save_var("user_profile", user_profile)

# Retrieve and modify the complex variable
retrieved_profile = load_var("user_profile")
print(f"User name: {retrieved_profile['name']}")
print(f"Theme preference: {retrieved_profile['preferences']['theme']}")

# Modify the variable
retrieved_profile["preferences"]["theme"] = "light"
save_var("user_profile", retrieved_profile)  # Store the updated version

# Check it was updated
updated_profile = load_var("user_profile")
print(f"Updated theme: {updated_profile['preferences']['theme']}")

# PART 5: Listing all stored variables
print("\n=== Listing All Stored Variables ===\n")
all_vars = list_vars()
print("Available debug variables:")
for name, type_name in all_vars.items():
    print(f"  - {name}: {type_name}")

print("\nDemo complete!")
