#!/usr/bin/env python
"""
Test script for document extraction service.
Usage: python test_extraction.py --file path/to/document.pdf
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# Add Django to path
sys.path.insert(0, str(Path(__file__).parent / 'django' / 'doccheck_service'))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doccheck_service.settings')
django.setup()

from cases.extraction_service import ExtractionService
from cases.models import VerificationDocument, VerificationCase


def test_extraction(file_path: str, document_key: str = 'caderneta_predial') -> None:
    """Test extraction on a single document."""
    if not os.path.exists(file_path):
        print(f" File not found: {file_path}")
        return

    print(f"\n📄 Testing extraction on: {file_path}")
    print(f"📋 Document type: {document_key}")
    print("=" * 60)

    # Run extraction
    print("\n⏳ Sending to Deepseek API...")
    result = ExtractionService.extract_from_file(file_path, document_key)

    # Display results
    print("\n✅ Extraction Results:")
    print("-" * 60)

    if result['success']:
        # Extracted fields
        print("\n📊 Extracted Fields:")
        fields = result.get('extracted_fields', {})
        for key, value in fields.items():
            print(f"  {key}: {value}")

        # Clarity assessment
        print("\n🔍 Clarity Assessment:")
        clarity = result.get('clarity_assessment', {})
        print(f"  Is Clear: {clarity.get('is_clear')}")
        print(f"  Legibility: {clarity.get('legibility')}%")
        print(f"  Confidence: {clarity.get('overall_confidence')}%")
        issues = clarity.get('issues', [])
        if issues:
            print(f"  Issues: {', '.join(issues)}")

        # Validity assessment
        print("\n✔️ Validity Assessment:")
        validity = result.get('validity_assessment', {})
        print(f"  Is Valid: {validity.get('is_valid')}")
        print(f"  Is Expired: {validity.get('is_expired')}")
        print(f"  Validity Period (months): {validity.get('validity_period_months')}")
        concerns = validity.get('concerns', [])
        if concerns:
            print(f"  Concerns: {', '.join(concerns)}")

        # AI Notes
        print("\n AI Notes:")
        print(f"  {result.get('notes', 'N/A')}")

        # Validation
        print("\n Validation Result:")
        validation = ExtractionService.validate_extracted_data(result)
        print(f"  Clarity Flag: {validation['clarity_flag']}")
        print(f"  Validity Flag: {validation['validity_flag']}")
        print(f"  Confidence Score: {validation['confidence_score']}")
        print(f"  Needs Manual Review: {validation['needs_manual_review']}")
        print(f"  All Fields Present: {validation['all_fields_present']}")

        print("\n✅ Extraction successful!")
    else:
        print(f"\n❌ Extraction failed!")
        print(f"Error: {result.get('error')}")

    print("\n" + "=" * 60)
    print("\n📋 Full JSON Response:")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def test_with_database(file_path: str, case_id: str, document_key: str = 'caderneta_predial') -> None:
    """Test extraction with database storage."""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    try:
        case = VerificationCase.objects.get(provider_case_id=case_id)
    except VerificationCase.DoesNotExist:
        print(f"❌ Case not found: {case_id}")
        print("\nCreate a case first:")
        print("  from cases.models import VerificationCase")
        print("  case = VerificationCase.objects.create(")
        print("      provider_case_id='dc_case_test',")
        print("      rezerva_reference_id='test_001',")
        print("      callback_url='https://webhook.local/doccheck',")
        print("      seller_name='Test Seller',")
        print("      seller_email='test@example.com'")
        print("  )")
        return

    print(f"\n📄 Testing extraction and database storage:")
    print(f"  Case: {case_id}")
    print(f"  Document: {document_key}")
    print(f"  File: {file_path}")
    print("=" * 60)

    # Extract
    result = ExtractionService.extract_from_file(file_path, document_key)

    if not result['success']:
        print(f"\n❌ Extraction failed: {result.get('error')}")
        return

    # Store in database
    doc, created = VerificationDocument.objects.get_or_create(
        provider_case=case,
        document_key=document_key,
    )

    doc.extracted_fields = result.get('extracted_fields', {})
    doc.clarity_assessment = result.get('clarity_assessment', {})
    doc.validity_assessment = result.get('validity_assessment', {})
    doc.extraction_notes = result.get('notes', '')

    validation = ExtractionService.validate_extracted_data(result)
    doc.clarity_flag = validation['clarity_flag']
    doc.validity_flag = validation['validity_flag']
    doc.confidence_score = validation['confidence_score']
    doc.needs_manual_review = validation['needs_manual_review']
    doc.all_fields_present = validation['all_fields_present']

    doc.extraction_status = 'success'
    doc.save()

    print(f"\n✅ Stored in database:")
    print(f"  Model: VerificationDocument")
    print(f"  ID: {doc.id}")
    print(f"  Clarity: {doc.clarity_flag} ({doc.confidence_score}%)")
    print(f"  Validity: {doc.validity_flag}")
    print(f"  Needs Review: {doc.needs_manual_review}")
    print("\n" + "=" * 60)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test document extraction service')
    parser.add_argument('--file', required=True, help='Path to document file')
    parser.add_argument('--document-key', default='caderneta_predial', help='Document key/type')
    parser.add_argument('--case-id', help='Case ID for database storage')
    parser.add_argument('--store', action='store_true', help='Store results in database')

    args = parser.parse_args()

    if args.store and args.case_id:
        test_with_database(args.file, args.case_id, args.document_key)
    else:
        test_extraction(args.file, args.document_key)
