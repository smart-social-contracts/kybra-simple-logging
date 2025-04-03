try:
    from kybra import ic
except:
    pass

import sys

from kybra_simple_logging import (
    save_var,
    load_var,
    list_vars,
    logger,
)


def custom_print(message: str):
    try:
        ic.print(message)
    except:
        print(message)


def test_save_load():
    """Test saving and loading variables"""
    custom_print("\n=== Testing save_load ===\n")
    
    # Test saving and loading a simple variable
    save_var("test_string", "Hello, World!")
    loaded_string = load_var("test_string")
    custom_print(f"Loaded string: {loaded_string}")
    assert loaded_string == "Hello, World!"
    
    # Test saving and loading a number
    save_var("test_number", 42)
    loaded_number = load_var("test_number")
    custom_print(f"Loaded number: {loaded_number}")
    assert loaded_number == 42
    
    # Test saving and loading a boolean
    save_var("test_bool", True)
    loaded_bool = load_var("test_bool")
    custom_print(f"Loaded boolean: {loaded_bool}")
    assert loaded_bool is True
    
    custom_print("Test passed!")
    return 0


def test_complex_objects():
    """Test storing and retrieving complex data structures"""
    custom_print("\n=== Testing complex_objects ===\n")
    
    # Test with dictionary
    test_dict = {"name": "Test User", "score": 42, "active": True}
    save_var("test_dict", test_dict)
    loaded_dict = load_var("test_dict")
    custom_print(f"Loaded dict: {loaded_dict}")
    assert loaded_dict["name"] == "Test User"
    assert loaded_dict["score"] == 42
    assert loaded_dict["active"] is True
    
    # Test with nested structures
    test_nested = {
        "user": {
            "id": 123,
            "tags": ["admin", "active"],
            "data": {
                "login_count": 5,
                "last_seen": "2025-04-01"
            }
        }
    }
    save_var("test_nested", test_nested)
    loaded_nested = load_var("test_nested")
    custom_print("Loaded nested object successfully")
    assert loaded_nested["user"]["id"] == 123
    assert "admin" in loaded_nested["user"]["tags"]
    assert loaded_nested["user"]["data"]["login_count"] == 5
    
    custom_print("Test passed!")
    return 0


def test_nonexistent():
    """Test behavior with non-existent variables"""
    custom_print("\n=== Testing nonexistent ===\n")
    
    # Test loading a non-existent variable returns None
    non_existent = load_var("does_not_exist")
    custom_print(f"Non-existent var returns: {non_existent}")
    assert non_existent is None
    
    custom_print("Test passed!")
    return 0


def test_list_vars():
    """Test listing all stored variables"""
    custom_print("\n=== Testing list_vars ===\n")
    
    # First clear any existing vars by replacing them
    save_var("var1", "test1")
    save_var("var2", 42)
    save_var("var3", {"a": 1, "b": 2})
    
    # Now get and check the list
    var_list = list_vars()
    custom_print(f"Variable list: {var_list}")
    
    # Check that all our vars are included with correct types
    assert "var1" in var_list
    assert "var2" in var_list
    assert "var3" in var_list
    assert var_list["var1"] == "str"
    assert var_list["var2"] == "int"
    assert var_list["var3"] == "dict"
    
    custom_print("Test passed!")
    return 0


def test_overwrite():
    """Test overwriting existing variables"""
    custom_print("\n=== Testing overwrite ===\n")
    
    # Save an initial value
    save_var("overwrite_test", "initial value")
    assert load_var("overwrite_test") == "initial value"
    
    # Overwrite with new value of same type
    save_var("overwrite_test", "new value")
    assert load_var("overwrite_test") == "new value"
    
    # Overwrite with different type
    save_var("overwrite_test", 123)
    assert load_var("overwrite_test") == 123
    
    custom_print("Test passed!")
    return 0


def run_all_tests():
    """Run all variable storage tests"""
    test_functions = [
        test_save_load,
        test_complex_objects,
        test_nonexistent,
        test_list_vars,
        test_overwrite
    ]
    
    failures = 0
    for test_func in test_functions:
        try:
            result = test_func()
            if result != 0:
                custom_print(f"Test {test_func.__name__} failed with code {result}")
                failures += 1
        except Exception as e:
            custom_print(f"Test {test_func.__name__} failed with exception: {e}")
            failures += 1
    
    custom_print(f"\n=== Variable Storage Tests Complete ===\n")
    custom_print(f"Ran {len(test_functions)} tests with {failures} failures")
    return failures


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific test if named
        test_name = sys.argv[1]
        if test_name in globals() and callable(globals()[test_name]):
            sys.exit(globals()[test_name]())
        else:
            custom_print(f"Test {test_name} not found")
            sys.exit(1)
    else:
        # Run all tests by default
        sys.exit(run_all_tests())
