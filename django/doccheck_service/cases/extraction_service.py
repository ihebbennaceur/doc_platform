"""
AI-powered document extraction service using Google Gemini API (free tier).
Extracts text, dates, names, issuer, and validates document content.
"""
from __future__ import annotations

import base64
import json
import logging
import os
from typing import Any

import requests

logger = logging.getLogger(__name__)

# Google Gemini API configuration
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent'

# Document extraction prompt template
EXTRACTION_PROMPT_TEMPLATE = """
You are a document verification expert. Analyze the provided document image/PDF and extract the following information in JSON format:

FIRST: Identify the document type from these options:
- caderneta_predial: Urban property registry from Finanças
- certidao_permanente: Permanent land registry certificate from Cartório
- certificado_energetico: Energy certificate from ADENE
- licenca_utilizacao: Usage license
- ficha_tecnica_habitacao: Housing technical file
- declaracao_condominio: Condominium statement
- distrate_hipoteca: Mortgage discharge
- habilitacao_herdeiros: Heirs qualification deed
- other: If none match

NOTE: The user submitted document type is: {user_selected_type}
Compare your detected type against this. If different, note clearly.

Response format:
{{
    "detected_document_type": "caderneta_predial or other type",
    "document_type_confidence": 0-100,
    "document_type_matches_user_selection": true or false,
    "detected_vs_user_selection": "Match, Mismatch, or Unclear",
    
    "extracted_fields": {{
        "name": "extracted person/entity name or null",
        "nif": "Portuguese tax ID or null",
        "date_issued": "YYYY-MM-DD or null",
        "date_expiry": "YYYY-MM-DD or null",
        "issuer": "issuing authority name or null",
        "reference_number": "document reference number or null",
        "property_reference": "property reference if applicable or null",
        "condominium": "condominium name if applicable or null",
        "unit_number": "apartment/unit number if applicable or null"
    }},
    
    "clarity_assessment": {{
        "is_clear": true or false,
        "legibility": 0-100,
        "overall_confidence": 0-100,
        "issues": []
    }},
    
    "validity_assessment": {{
        "is_valid": true or false,
        "is_expired": true, false, or unknown,
        "validity_period_months": null,
        "concerns": []
    }},
    
    "notes": "Any additional observations about the document"
}}

Rules:
1. Detect document type from visual cues: layout, logos, official seals, field names
2. Compare detected type with user selection - flag if mismatch
3. Extract all visible fields, mark as null if not found
4. Respond ONLY with valid JSON, no additional text.
"""



class ExtractionService:
    """Handle document extraction using AI."""

    @staticmethod
    def extract_from_file(file_path: str, document_type: str = 'unknown', user_selected_document_type: str = '') -> dict[str, Any]:
        """
        Extract information from a document file (PDF or image).

        Args:
            file_path: Path to the document file
            document_type: Type of document (caderneta_predial, certidao_permanente, etc.)
            user_selected_document_type: Document type selected by user (for comparison with AI detection)

        Returns:
            Dictionary with extracted data, confidence scores, and validity assessment
        """
        try:
            logger.info(f"[ExtractionService] Starting extraction for {file_path}")

            # Read file and convert to base64
            with open(file_path, 'rb') as f:
                file_data = f.read()
            file_base64 = base64.b64encode(file_data).decode('utf-8')

            # Determine media type
            if file_path.lower().endswith('.pdf'):
                media_type = 'application/pdf'
            elif file_path.lower().endswith(('.jpg', '.jpeg')):
                media_type = 'image/jpeg'
            elif file_path.lower().endswith('.png'):
                media_type = 'image/png'
            else:
                media_type = 'application/octet-stream'

            logger.info(f"[ExtractionService] File media type: {media_type}")

            # Format prompt with user's document type selection
            formatted_prompt = EXTRACTION_PROMPT_TEMPLATE.format(
                user_selected_type=user_selected_document_type or 'not specified'
            )

            # Call Google Gemini API
            payload = {
                'contents': [
                    {
                        'role': 'user',
                        'parts': [
                            {'text': formatted_prompt},
                            {
                                'inline_data': {
                                    'mime_type': media_type,
                                    'data': file_base64,
                                }
                            }
                        ]
                    }
                ],
                'generationConfig': {
                    'temperature': 0.3,
                    'maxOutputTokens': 1000,
                }
            }

            headers = {'Content-Type': 'application/json'}
            url = f"{GEMINI_API_URL}?key={GOOGLE_API_KEY}"

            logger.info('[ExtractionService] Calling Google Gemini API...')
            response = requests.post(url, json=payload, headers=headers, timeout=30)

            if response.status_code != 200:
                error_msg = f"Gemini API error: {response.status_code} - {response.text}"
                logger.error(f'[ExtractionService] {error_msg}')
                return {
                    'success': False,
                    'error': error_msg,
                    'extracted_fields': {},
                    'clarity_assessment': {'overall_confidence': 0, 'is_clear': False},
                    'validity_assessment': {'is_valid': False},
                    'notes': 'AI extraction failed - manual review required',
                }

            result = response.json()
            logger.info(f'[ExtractionService] Gemini API response: {json.dumps(result, indent=2)[:500]}...')

            # Parse response - Gemini returns candidates with content in parts
            if 'candidates' not in result or not result['candidates']:
                error_msg = 'Unexpected Gemini API response format'
                logger.error(f'[ExtractionService] {error_msg}')
                return {
                    'success': False,
                    'error': error_msg,
                    'extracted_fields': {},
                    'clarity_assessment': {'overall_confidence': 0, 'is_clear': False},
                    'validity_assessment': {'is_valid': False},
                    'notes': 'AI parsing error - manual review required',
                }

            # Extract text from Gemini response
            candidate = result['candidates'][0]
            if 'content' not in candidate or 'parts' not in candidate['content']:
                error_msg = 'Unexpected Gemini response structure'
                logger.error(f'[ExtractionService] {error_msg}')
                return {
                    'success': False,
                    'error': error_msg,
                    'extracted_fields': {},
                    'clarity_assessment': {'overall_confidence': 0, 'is_clear': False},
                    'validity_assessment': {'is_valid': False},
                    'notes': 'AI parsing error - manual review required',
                }

            content = candidate['content']['parts'][0]['text']
            logger.info(f'[ExtractionService] Raw content: {content[:200]}...')

            # Parse JSON from response
            try:
                extracted_data = json.loads(content)
                logger.info(f'[ExtractionService] Successfully parsed extraction: {json.dumps(extracted_data, indent=2)[:300]}...')
            except json.JSONDecodeError as e:
                error_msg = f'Failed to parse AI response as JSON: {str(e)}'
                logger.error(f'[ExtractionService] {error_msg}')
                return {
                    'success': False,
                    'error': error_msg,
                    'extracted_fields': {},
                    'clarity_assessment': {'overall_confidence': 0, 'is_clear': False},
                    'validity_assessment': {'is_valid': False},
                    'notes': 'AI response parsing error - manual review required',
                }

            return {
                'success': True,
                'extracted_fields': extracted_data.get('extracted_fields', {}),
                'clarity_assessment': extracted_data.get('clarity_assessment', {}),
                'validity_assessment': extracted_data.get('validity_assessment', {}),
                'document_type': extracted_data.get('document_type', 'unknown'),
                'notes': extracted_data.get('notes', ''),
            }

        except Exception as e:
            error_msg = f'Extraction service error: {str(e)}'
            logger.error(f'[ExtractionService] {error_msg}', exc_info=True)
            return {
                'success': False,
                'error': error_msg,
                'extracted_fields': {},
                'clarity_assessment': {'overall_confidence': 0, 'is_clear': False},
                'validity_assessment': {'is_valid': False},
                'notes': 'System error during extraction - manual review required',
            }

    @staticmethod
    def validate_extracted_data(extracted_data: dict[str, Any]) -> dict[str, Any]:
        """
        Validate extracted data and generate validity verdict.

        Returns:
            Dictionary with validation results and clarity flags
        """
        clarity = extracted_data.get('clarity_assessment', {})
        validity = extracted_data.get('validity_assessment', {})

        is_clear = clarity.get('is_clear', False)
        confidence = clarity.get('overall_confidence', 0)
        is_valid = validity.get('is_valid', False)
        is_expired = validity.get('is_expired', False)

        # Determine clarity flag
        clarity_flag = 'CLEAR' if is_clear and confidence > 80 else ('UNCLEAR' if confidence < 50 else 'PARTIAL')

        # Determine validity flag
        validity_flag = 'VALID' if is_valid and not is_expired else ('EXPIRED' if is_expired else 'INVALID')

        return {
            'clarity_flag': clarity_flag,
            'validity_flag': validity_flag,
            'confidence_score': confidence,
            'needs_manual_review': not is_clear or confidence < 70 or not is_valid,
            'all_fields_present': bool(
                extracted_data.get('extracted_fields', {}).get('name')
                and extracted_data.get('extracted_fields', {}).get('date_issued')
            ),
        }
