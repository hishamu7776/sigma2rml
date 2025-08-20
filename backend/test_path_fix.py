#!/usr/bin/env python3
"""
Test path handling fix for file viewing issue
"""

import sys
import os

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_path_resolution():
    """Test path resolution functions"""
    print("=== Testing Path Resolution ===")
    
    try:
        from app.api.files import resolve_path, normalize_path
        
        # Test path normalization
        test_paths = [
            "uploaded_files\\test.yml",
            "uploaded_files/test.yml",
            "C:\\Users\\test\\file.yml",
            "/home/user/file.yml"
        ]
        
        for path in test_paths:
            normalized = normalize_path(path)
            resolved = resolve_path(normalized)
            print(f"Original: {path}")
            print(f"Normalized: {normalized}")
            print(f"Resolved: {resolved}")
            print(f"OS: {os.name}")
            print("---")
        
        print("✅ Path resolution test completed")
        
    except Exception as e:
        print(f"❌ Path resolution test failed: {e}")

def test_file_registry():
    """Test current file registry"""
    print("\n=== Testing File Registry ===")
    
    try:
        from app.storage.db import load_db
        
        db = load_db()
        print(f"Found {len(db)} files in registry")
        
        for file_info in db:
            print(f"File: {file_info['filename']}")
            print(f"Stored path: {file_info['path']}")
            
            # Test if we can resolve the path
            from app.api.files import resolve_path
            actual_path = resolve_path(file_info['path'])
            print(f"Resolved path: {actual_path}")
            
            # Check if file exists
            if os.path.exists(actual_path):
                print("✅ File exists")
            else:
                print("❌ File not found")
            print("---")
        
        print("✅ File registry test completed")
        
    except Exception as e:
        print(f"❌ File registry test failed: {e}")

if __name__ == "__main__":
    test_path_resolution()
    test_file_registry()
