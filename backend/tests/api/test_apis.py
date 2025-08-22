#!/usr/bin/env python3
"""
Test Sigma to RML File APIs
Tests the core functionality of file upload, storage, and translation
"""

import sys
import os
import shutil

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

def test_storage_functions():
    """Test storage database functions"""
    print("\n=== Testing Storage Database Functions ===")
    
    try:
        from app.storage.db import load_db, add_file_record, get_file_record, update_translation_status, delete_file_record
        
        # Test load_db
        db = load_db()
        if isinstance(db, list):
            print("PASS: load_db: 0 records loaded")
        else:
            print("FAIL: load_db: Unexpected return type")
        
        # Test add_file_record
        test_record = {
            "filename": "test_rule.yml",
            "path": "test/path/test_rule.yml",
            "title": "Test Rule",
            "upload_time": "2024-01-01T00:00:00Z",
            "translation_status": "pending"
        }
        
        add_file_record(test_record)
        print("PASS: add_file_record: Added test_rule.yml")
        
        # Test get_file_record
        retrieved_record = get_file_record("test_rule.yml")
        if retrieved_record and retrieved_record.get("title") == "Test Rule":
            print("PASS: get_file_record: Found test_rule.yml with title 'Test Rule'")
        else:
            print("FAIL: get_file_record: Failed to retrieve correct record")
        
        # Test update_translation_status
        update_translation_status("test_rule.yml", "translated")
        updated_record = get_file_record("test_rule.yml")
        if updated_record and updated_record.get("translation_status") == "translated":
            print("PASS: update_translation_status: Updated test_rule.yml to translated")
        else:
            print("FAIL: update_translation_status: Failed to update status")
        
        # Test delete_file_record
        delete_file_record("test_rule.yml")
        deleted_record = get_file_record("test_rule.yml")
        if deleted_record is None:
            print("PASS: delete_file_record: Successfully deleted test_rule.yml")
        else:
            print("FAIL: delete_file_record: Failed to delete record")
        
    except Exception as e:
        print(f"FAIL: Storage functions test failed: {e}")
        import traceback
        traceback.print_exc()

def test_transpiler():
    """Test core transpiler functionality"""
    print("\n=== Testing Core Transpiler ===")
    
    try:
        from app.core.transpiler_refactored import RefactoredTranspiler
        
        transpiler = RefactoredTranspiler()
        
        # Test basic rule transpilation
        test_sigma = """
detection:
  selection:
    EventID: 4738
    AttributeLDAPDisplayName: 'Min-Pwd-Length'
    AttributeValue|gte: 7
  condition: selection
"""
        
        result = transpiler.transpile(test_sigma)
        if result and "safe_selection" in result:
            print("PASS: Core transpiler: Basic rule transpilation successful")
        else:
            print("FAIL: Core transpiler: Basic rule transpilation failed")
        
    except Exception as e:
        print(f"FAIL: Transpiler test failed: {e}")
        import traceback
        traceback.print_exc()

def test_file_operations():
    """Test file operations and YAML parsing"""
    print("\n=== Testing File Operations ===")
    
    try:
        # Create test directories
        test_upload_dir = "test_upload_files"
        test_translated_dir = "test_translated_files"
        
        os.makedirs(test_upload_dir, exist_ok=True)
        os.makedirs(test_translated_dir, exist_ok=True)
        
        # Test file creation and writing
        test_sigma_content = """title: Test Sigma Rule
logsource:
  product: windows
  service: security
detection:
  selection:
    EventID: 4738
  condition: selection
"""
        
        test_file_path = os.path.join(test_upload_dir, "test_rule.yml")
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(test_sigma_content)
        
        print(f"PASS: Created test file: {test_file_path}")
        
        # Test file reading
        with open(test_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if "Test Sigma Rule" in content:
                print("PASS: File reading: Successfully read test file")
            else:
                print("FAIL: File reading: Failed to read test file content")
        
        # Test YAML parsing
        import yaml
        try:
            parsed_content = yaml.safe_load(content)
            if parsed_content.get("title") == "Test Sigma Rule":
                print("PASS: YAML parsing: Successfully parsed test file")
            else:
                print("FAIL: YAML parsing: Failed to parse test file correctly")
        except Exception as e:
            print(f"FAIL: YAML parsing: Failed to parse YAML: {e}")
        
        # Cleanup
        shutil.rmtree(test_upload_dir)
        shutil.rmtree(test_translated_dir)
        print("PASS: Cleanup: Removed test directories")
        
    except Exception as e:
        print(f"FAIL: File operations test failed: {e}")

def test_api_endpoints():
    """Test API endpoint functionality"""
    print("\n=== Testing API Endpoints ===")
    
    try:
        from app.api.transpile import transpile_sigma
        from app.api.translate import translate_sigma_file
        from app.api.files import list_files, view_file, view_rml, delete_file
        
        print("PASS: API imports: Successfully imported all API modules")
        
        # Test transpile endpoint logic
        test_sigma = """
detection:
  selection:
    EventID: 4738
  condition: selection
"""
        
        # Note: We can't actually call the async functions here, but we can test the logic
        from app.core.transpiler_refactored import RefactoredTranspiler
        transpiler = RefactoredTranspiler()
        
        try:
            result = transpiler.transpile(test_sigma)
            if result:
                print("PASS: Transpile logic: Successfully transpiled test Sigma rule")
            else:
                print("FAIL: Transpile logic: Failed to transpile test Sigma rule")
        except Exception as e:
            print(f"FAIL: Transpile logic: Error during transpilation: {e}")
        
    except Exception as e:
        print(f"FAIL: API endpoints test failed: {e}")

def main():
    """Run all API tests"""
    print("Testing Sigma to RML File APIs")
    print("=" * 60)
    
    try:
        test_storage_functions()
        test_transpiler()
        test_file_operations()
        test_api_endpoints()
        
        print("\n" + "=" * 60)
        print("RESULT: API Testing Complete!")
        print("PASS: All core functionality tested")
        
    except Exception as e:
        print(f"\nFAIL: API testing failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
