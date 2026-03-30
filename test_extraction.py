#!/usr/bin/env python
"""
Test the document extraction workflow
"""
import os
import sys
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
sys.path.insert(0, 'c:\\Users\\send6\\Desktop\\pfe_seller_platform\\backend_django\\backend_seller_platform\\myproject')
django.setup()

from accounts.models import Document, User

# Get the first document
docs = Document.objects.all()[:1]
if not docs:
    print("[ERROR] No documents found")
    sys.exit(1)

doc = docs[0]
print(f"[INFO] Testing document: {doc.file.name}")
print(f"[INFO]    ID: {doc.id}")
print(f"[INFO]    Type: {doc.document_type}")
print(f"[INFO]    File: {doc.file.path if doc.file else 'No file'}")
print(f"[INFO]    Current extracted_fields: {doc.extracted_fields}")

# Test extraction
if doc.file and os.path.exists(doc.file.path):
    print("\n[RUNNING] Starting extraction...")
    try:
        sys.path.insert(0, 'c:\\Users\\send6\\Desktop\\pfe_seller_platform\\django\\doccheck_service')
        from cases.extraction_service import ExtractionService
        
        result = ExtractionService.extract_from_file(
            doc.file.path,
            doc.document_type
        )
        
        print(f"\n[SUCCESS] Extraction result:")
        print(json.dumps(result, indent=2))
        
        if result.get('success') or result.get('extracted_fields'):
            print("\n[FIELDS] Extracted fields:")
            print(json.dumps(result.get('extracted_fields', {}), indent=2))
    except Exception as e:
        print(f"[ERROR] Extraction error: {e}")
        import traceback
        traceback.print_exc()
else:
    print(f"[ERROR] File not found: {doc.file.path if doc.file else 'No file'}")
