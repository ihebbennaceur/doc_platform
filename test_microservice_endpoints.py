#!/usr/bin/env python
"""Test the document upload endpoint."""

import requests
import json

BASE_URL = "http://127.0.0.1:8001/api"

def test_case_creation():
    """First, create a case."""
    print("\n=== Testing Case Creation ===")
    payload = {
        "rezerva_reference_id": "test-ref-001",
        "seller_info": {
            "email": "seller@example.com",
            "name": "Test Seller",
            "nif": "123456789"
        },
        "required_documents": ["caderneta", "certidao"],
        "assessment_data": {
            "property_type": "apartment",
            "building_construction": "1991_2007",
            "acquisition_type": "purchase"
        }
    }
    
    response = requests.post(f"{BASE_URL}/cases/", json=payload)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(json.dumps(data, indent=2))
    
    if response.status_code in [200, 201]:
        case_id = data.get("provider_case_id")
        return case_id
    return None


def test_document_upload(case_id: str):
    """Test uploading a document to a case."""
    if not case_id:
        print("No case ID provided, skipping upload test")
        return
    
    print(f"\n=== Testing Document Upload to Case {case_id} ===")
    
    # Create a simple test file
    test_file_path = "/tmp/test_document.txt"
    with open(test_file_path, "w") as f:
        f.write("This is a test document for verification.")
    
    # Prepare multipart form data
    with open(test_file_path, "rb") as f:
        files = {"file": (f"test_document.txt", f, "text/plain")}
        data = {"document_key": "caderneta"}
        
        response = requests.post(
            f"{BASE_URL}/cases/{case_id}/documents/upload",
            files=files,
            data=data
        )
    
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    print("Testing DocCheck Microservice Endpoints")
    case_id = test_case_creation()
    test_document_upload(case_id)
