#!/usr/bin/env python
"""Test the microservice using Django's test client."""

import os
import sys
import django
import uuid

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doccheck_service.settings')
django.setup()

from django.test import Client
from django.middleware.csrf import get_token
import json

client = Client()

# Get CSRF token for POST requests
print("\n=== Testing API Root ===")
response = client.get('/api/')
print(f"Status: {response.status_code}")
print(f"Content-Type: {response.get('Content-Type')}")
print(f"Body: {response.content.decode()[:200]}")

print("\n=== Testing Case Creation ===")
case_ref_id = f"test-ref-{uuid.uuid4().hex[:8]}"
payload = {
    "rezerva_reference_id": case_ref_id,
    "seller_info": {
        "email": "test@example.com",
        "name": "Test Seller",
        "nif": "123456789"
    },
    "required_documents": ["caderneta", "certidao"]
}
# API endpoints should not require CSRF, but let's test
response = client.post(
    '/api/cases/',
    data=json.dumps(payload),
    content_type='application/json',
    HTTP_ACCEPT='application/json'
)
print(f"Status: {response.status_code}")
print(f"Body: {response.content.decode()}")
if response.status_code in [200, 201]:
    data = json.loads(response.content)
    case_id = data.get('provider_case_id')
    print(f"\nCreated case: {case_id}")
    
    print("\n=== Testing Document Upload ===")
    # Create a test file
    from django.core.files.uploadedfile import SimpleUploadedFile
    test_file = SimpleUploadedFile(
        "test.pdf",
        b"test content",
        content_type="application/pdf"
    )
    response = client.post(
        f'/api/cases/{case_id}/documents/upload',
        {'document_key': 'caderneta', 'file': test_file}
    )
    print(f"Status: {response.status_code}")
    print(f"Body: {response.content.decode()}")
