#!/usr/bin/env python3
"""
Final validation test for empty filename handling
"""

import sys
import os

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_empty_filename_handling():
    """Test that empty filenames are properly handled"""
    print("=== Testing Empty Filename Handling ===")
    
    try:
        from app.storage.db import get_file_record, add_file_record, delete_file_record, update_translation_status
        
        # Test get_file_record with empty filename
        try:
            record = get_file_record("")
            if record is None:
                print("✅ get_file_record: Correctly returns None for empty filename")
            else:
                print("❌ get_file_record: Should return None for empty filename")
        except Exception as e:
            print(f"✅ get_file_record: Correctly handled empty filename with error: {type(e).__name__}")
        
        # Test add_file_record with empty filename
        try:
            add_file_record("", "/test/path", "Test")
            print("❌ add_file_record: Should have failed with empty filename")
        except ValueError as e:
            if "cannot be empty" in str(e):
                print("✅ add_file_record: Correctly rejected empty filename")
            else:
                print(f"❌ add_file_record: Unexpected error message: {e}")
        except Exception as e:
            print(f"✅ add_file_record: Correctly handled empty filename with error: {type(e).__name__}")
        
        # Test delete_file_record with empty filename
        try:
            delete_file_record("")
            print("❌ delete_file_record: Should have failed with empty filename")
        except ValueError as e:
            if "cannot be empty" in str(e):
                print("✅ delete_file_record: Correctly rejected empty filename")
            else:
                print(f"❌ delete_file_record: Unexpected error message: {e}")
        except Exception as e:
            print(f"✅ delete_file_record: Correctly handled empty filename with error: {type(e).__name__}")
        
        # Test update_translation_status with empty filename
        try:
            update_translation_status("", "/test/path.rml")
            print("❌ update_translation_status: Should have failed with empty filename")
        except ValueError as e:
            if "cannot be empty" in str(e):
                print("✅ update_translation_status: Correctly rejected empty filename")
            else:
                print(f"❌ update_translation_status: Unexpected error message: {e}")
        except Exception as e:
            print(f"✅ update_translation_status: Correctly handled empty filename with error: {type(e).__name__}")
        
        print("\n🎯 Empty filename validation test complete!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    test_empty_filename_handling()
