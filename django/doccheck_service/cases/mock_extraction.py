"""
Mock extraction service for testing - returns sample extracted data
"""
import json
from typing import Any

def get_mock_extracted_fields(document_type: str) -> dict[str, Any]:
    """Return mock extracted fields based on document type"""
    
    mock_data = {
        'id': {
            'full_name': 'John David Smith',
            'id_number': 'ID123456',
            'date_of_birth': '1985-03-15',
            'issue_date': '2020-01-10',
            'expiry_date': '2030-01-10',
            'nationality': 'Portuguese',
        },
        'license': {
            'license_number': 'LIC-2024-00123',
            'issued_to': 'Jane Doe',
            'issue_date': '2022-06-01',
            'expiry_date': '2025-06-01',
            'license_type': 'Professional',
        },
        'proof_of_address': {
            'address': 'Rua da Rosa 123, 1000-000 Lisboa',
            'resident_name': 'Maria Silva',
            'issue_date': '2024-01-15',
            'utility_provider': 'EDP - Energias de Portugal',
            'reference_number': 'UTIL-2024-456789',
        },
        'other': {
            'document_name': 'Other Document',
            'extracted_text': 'Document content successfully extracted',
            'extraction_date': '2024-03-30',
        }
    }
    
    return mock_data.get(document_type, mock_data['other'])


def extract_from_file_mock(file_path: str, document_type: str = 'unknown') -> dict[str, Any]:
    """Mock extraction function that returns sample data"""
    
    try:
        extracted_fields = get_mock_extracted_fields(document_type)
        
        return {
            'success': True,
            'extracted_fields': extracted_fields,
            'clarity_assessment': {
                'overall_confidence': 95,
                'is_clear': True,
                'legibility': 98,
                'issues': []
            },
            'validity_assessment': {
                'is_valid': True,
                'is_expired': False,
                'validity_period_months': None,
                'concerns': []
            },
            'document_type': document_type,
            'notes': 'Mock extraction - sample data for testing',
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'extracted_fields': {},
            'clarity_assessment': {'overall_confidence': 0, 'is_clear': False},
            'validity_assessment': {'is_valid': False},
            'notes': 'Mock extraction failed',
        }
