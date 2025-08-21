#!/usr/bin/env python3
"""
Test RML endpoint fix
"""

import sys
import os

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_rml_endpoint():
    """Test that both RML endpoints work"""
    print("=== Testing RML Endpoints ===")
    
    try:
        from app.api.files import view_rml, view_rml_legacy
        from app.storage.db import get_file_record
        
        # Test with the existing file
        filename = "file_access_win_susp_credential_manager_access.yml"
        
        print(f"Testing file: {filename}")
        
        # Check if file exists in registry
        record = get_file_record(filename)
        if record:
            print(f"PASS File found in registry")
            print(f"   Translated: {record.get('translated')}")
            print(f"   RML path: {record.get('rml_path')}")
        else:
            print("FAIL File not found in registry")
            return
        
        # Test the legacy endpoint (what frontend uses)
        try:
            result = view_rml_legacy(filename)
            print("PASS Legacy endpoint (/rml/{filename}) works")
            print(f"   RML content length: {len(result.get('rml', ''))}")
        except Exception as e:
            print(f"FAIL Legacy endpoint failed: {e}")
        
        # Test the new endpoint
        try:
            result = view_rml(filename)
            print("PASS New endpoint (/{filename}/rml) works")
            print(f"   RML content length: {len(result.get('rml', ''))}")
        except Exception as e:
            print(f"FAIL New endpoint failed: {e}")
        
        print("\nRESULT RML endpoint test completed!")
        
    except Exception as e:
        print(f"FAIL Test failed with error: {e}")

if __name__ == "__main__":
    test_rml_endpoint()
