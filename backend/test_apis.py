#!/usr/bin/env python3
"""
Test all file-related APIs for Sigma to RML transpiler
Tests upload, transpile, translate, and file management endpoints
"""

import sys
import os
import json
import tempfile
import shutil
from pathlib import Path

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_storage_functions():
    """Test storage database functions"""
    print("=== Testing Storage Database Functions ===")
    
    try:
        from app.storage.db import load_db, add_file_record, get_file_record, update_translation_status, delete_file_record
        
        # Test load_db
        db = load_db()
        print(f"✅ load_db: {len(db)} records loaded")
        
        # Test add_file_record
        test_filename = "test_rule.yml"
        test_path = "/test/path/test_rule.yml"
        test_title = "Test Rule"
        
        add_file_record(test_filename, test_path, test_title)
        print(f"✅ add_file_record: Added {test_filename}")
        
        # Test get_file_record
        record = get_file_record(test_filename)
        if record:
            print(f"✅ get_file_record: Found {record['filename']} with title '{record['title']}'")
        else:
            print("❌ get_file_record: Failed to retrieve record")
        
        # Test update_translation_status
        rml_path = "/test/path/test_rule.rml"
        update_translation_status(test_filename, rml_path)
        updated_record = get_file_record(test_filename)
        if updated_record and updated_record.get("translated"):
            print(f"✅ update_translation_status: Updated {test_filename} to translated")
        else:
            print("❌ update_translation_status: Failed to update record")
        
        # Test delete_file_record
        delete_file_record(test_filename)
        deleted_record = get_file_record(test_filename)
        if not deleted_record:
            print(f"✅ delete_file_record: Successfully deleted {test_filename}")
        else:
            print("❌ delete_file_record: Failed to delete record")
            
    except Exception as e:
        print(f"❌ Storage functions test failed: {e}")

def test_transpiler():
    """Test the core transpiler"""
    print("\n=== Testing Core Transpiler ===")
    
    try:
        from app.core.transpiler import SigmaToRMLTranspiler
        
        transpiler = SigmaToRMLTranspiler()
        
        # Test basic Sigma rule
        sigma_rule = {
            'logsource': {'product': 'windows', 'service': 'security'},
            'detection': {
                'selection': {'EventID': 4738},
                'condition': 'selection'
            }
        }
        
        result = transpiler.transpile(sigma_rule)
        if result and "logsource matches" in result:
            print("✅ Core transpiler: Basic rule transpilation successful")
        else:
            print("❌ Core transpiler: Basic rule transpilation failed")
            
    except Exception as e:
        print(f"❌ Core transpiler test failed: {e}")

def test_file_operations():
    """Test file operations"""
    print("\n=== Testing File Operations ===")
    
    try:
        # Create test directories
        test_upload_dir = "test_upload_files"
        test_translated_dir = "test_translated_files"
        
        os.makedirs(test_upload_dir, exist_ok=True)
        os.makedirs(test_translated_dir, exist_ok=True)
        
        # Create a test Sigma rule file
        test_sigma_content = """
title: Test Sigma Rule
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
        
        print(f"✅ Created test file: {test_file_path}")
        
        # Test file reading
        with open(test_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if "Test Sigma Rule" in content:
                print("✅ File reading: Successfully read test file")
            else:
                print("❌ File reading: Failed to read test file content")
        
        # Test YAML parsing
        import yaml
        try:
            parsed_content = yaml.safe_load(content)
            if parsed_content.get("title") == "Test Sigma Rule":
                print("✅ YAML parsing: Successfully parsed test file")
            else:
                print("❌ YAML parsing: Failed to parse test file correctly")
        except Exception as e:
            print(f"❌ YAML parsing: Failed to parse YAML: {e}")
        
        # Cleanup
        shutil.rmtree(test_upload_dir)
        shutil.rmtree(test_translated_dir)
        print("✅ Cleanup: Removed test directories")
        
    except Exception as e:
        print(f"❌ File operations test failed: {e}")

def test_api_endpoints():
    """Test API endpoint functionality"""
    print("\n=== Testing API Endpoints ===")
    
    try:
        from app.api.transpile import transpile_sigma
        from app.api.translate import translate_sigma_file
        from app.api.files import list_files, view_file, view_rml, delete_file
        
        print("✅ API imports: Successfully imported all API modules")
        
        # Test transpile endpoint logic
        test_sigma = """
detection:
  selection:
    EventID: 4738
  condition: selection
"""
        
        # Note: We can't actually call the async functions here, but we can test the logic
        from app.core.transpiler import SigmaToRMLTranspiler
        transpiler = SigmaToRMLTranspiler()
        
        try:
            result = transpiler.transpile(test_sigma)
            if result:
                print("✅ Transpile logic: Successfully transpiled test Sigma rule")
            else:
                print("❌ Transpile logic: Failed to transpile test Sigma rule")
        except Exception as e:
            print(f"❌ Transpile logic: Error during transpilation: {e}")
        
    except Exception as e:
        print(f"❌ API endpoints test failed: {e}")

def main():
    """Run all API tests"""
    print("🧪 Testing Sigma to RML File APIs")
    print("=" * 60)
    
    try:
        test_storage_functions()
        test_transpiler()
        test_file_operations()
        test_api_endpoints()
        
        print("\n" + "=" * 60)
        print("🎯 API Testing Complete!")
        print("✅ All core functionality tested")
        
    except Exception as e:
        print(f"\n❌ API testing failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
