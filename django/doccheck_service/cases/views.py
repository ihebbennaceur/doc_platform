from __future__ import annotations

from typing import Any, Dict
import os

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import VerificationCase, VerificationDocument, DocumentValidity
from .serializers import (
    CaseStatusUpdateSerializer,
    VerificationCaseCreateSerializer,
    VerificationCaseDetailSerializer,
    VerificationCaseResponseSerializer,
    VerificationDocumentSerializer,
)
from .extraction_service import ExtractionService


class APIRootView(APIView):
    """Return hypermedia links for available DocCheck endpoints."""

    def get(self, request, *args: Any, **kwargs: Any) -> Response:
        return Response(
            {
                'create_case': request.build_absolute_uri(reverse('cases:case-create')),
                'case_detail': request.build_absolute_uri('/api/cases/{provider_case_id}/'),
                'case_status_update': request.build_absolute_uri(
                    '/api/cases/{provider_case_id}/status/'
                ),
            }
        )


class VerificationCaseCreateView(APIView):
    """Accept Rezerva case creation payloads."""

    def post(self, request, *args: Any, **kwargs: Any) -> Response:
        serializer = VerificationCaseCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        seller = validated['seller']
        # Support both 'full_name' (API) and 'name' (frontend)
        seller_name = seller.get('full_name') or seller.get('name') or 'Unknown'
        seller_email = seller.get('email') or 'unknown@example.com'
        seller_phone = seller.get('phone') or ''
        
        case = VerificationCase.objects.create(
            rezerva_reference_id=validated['rezerva_reference_id'],
            callback_url=validated['callback_url'],
            seller_name=seller_name,
            seller_email=seller_email,
            seller_phone=seller_phone,
            metadata={
                'required_documents': validated.get('required_documents', []),
                'assessment_data': validated.get('assessment_data', {}),
            },
        )

        documents = [
            VerificationDocument(provider_case=case, document_key=doc_key)
            for doc_key in validated.get('required_documents', [])
        ]
        VerificationDocument.objects.bulk_create(documents)

        response_serializer = VerificationCaseResponseSerializer(
            case,
            context={'upload_base': self._upload_base(request)},
        )
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def _upload_base(request) -> str:
        return request.build_absolute_uri('/upload')


class VerificationCaseDetailView(APIView):
    def get(self, request, provider_case_id: str, *args: Any, **kwargs: Any) -> Response:
        case = get_object_or_404(VerificationCase, provider_case_id=provider_case_id)
        serializer = VerificationCaseDetailSerializer(case)
        return Response(serializer.data)


class CaseStatusUpdateView(APIView):
    def patch(self, request, provider_case_id: str, *args: Any, **kwargs: Any) -> Response:
        case = get_object_or_404(VerificationCase, provider_case_id=provider_case_id)
        serializer = CaseStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        case.status = validated['status']
        if validated.get('overall_reason'):
            metadata: Dict[str, Any] = case.metadata or {}
            metadata['overall_reason'] = validated['overall_reason']
            case.metadata = metadata
        case.save()

        for document in validated.get('documents', []):
            doc_obj, _ = VerificationDocument.objects.get_or_create(
                provider_case=case,
                document_key=document['document_key'],
            )
            doc_obj.status = document['status']
            doc_obj.reason = document.get('reason', '')
            doc_obj.save()

        detail_serializer = VerificationCaseDetailSerializer(case)
        return Response(detail_serializer.data)


class DocumentUploadView(APIView):
    """Handle document upload for a case."""
    parser_classes = (MultiPartParser, FormParser)

    def post(
        self, request, provider_case_id: str, *args: Any, **kwargs: Any
    ) -> Response:
        case = get_object_or_404(VerificationCase, provider_case_id=provider_case_id)
        
        # Get document_key, file, and user-selected document type from request
        document_key = request.POST.get('document_key', '').lower()
        uploaded_file = request.FILES.get('file')
        user_selected_document_type = request.POST.get('document_type', '').strip()
        
        if not document_key or not uploaded_file:
            return Response(
                {'error': 'document_key and file are required'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        # Validate MIME type (allow PDF and images only)
        allowed_types = ['application/pdf', 'image/jpeg', 'image/png', 'image/tiff']
        if uploaded_file.content_type not in allowed_types:
            return Response(
                {'error': f'Invalid file type: {uploaded_file.content_type}. Allowed: PDF, JPEG, PNG, TIFF'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        # Get or create document record
        doc_obj, _ = VerificationDocument.objects.get_or_create(
            provider_case=case,
            document_key=document_key,
        )
        
        # Store file locally in media folder
        from django.conf import settings
        media_root = settings.MEDIA_ROOT
        case_media_dir = os.path.join(media_root, 'cases', case.provider_case_id, document_key)
        os.makedirs(case_media_dir, exist_ok=True)
        
        # Save file
        file_path = os.path.join(case_media_dir, uploaded_file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        # Store file metadata
        doc_obj.file_name = uploaded_file.name
        doc_obj.file_size = uploaded_file.size
        doc_obj.mime_type = uploaded_file.content_type
        doc_obj.file_path = os.path.relpath(file_path, media_root)  # relative path for DB
        doc_obj.uploaded_at = timezone.now()
        doc_obj.status = VerificationDocument.DocumentStatus.PROCESSING
        doc_obj.extraction_status = 'processing'
        doc_obj.user_submitted_document_type = user_selected_document_type  # Store user's selection
        doc_obj.save()
        
        # Trigger AI extraction (async would be ideal, but doing synchronous for now)
        # Pass user's document type selection to extraction service
        extraction_result = ExtractionService.extract_from_file(
            file_path, 
            document_key,
            user_selected_document_type=user_selected_document_type
        )
        
        if extraction_result['success']:
            # Extract and store results
            extracted_fields = extraction_result.get('extracted_fields', {})
            clarity = extraction_result.get('clarity_assessment', {})
            validity = extraction_result.get('validity_assessment', {})
            
            doc_obj.extracted_fields = extracted_fields
            doc_obj.clarity_assessment = clarity
            doc_obj.validity_assessment = validity
            doc_obj.extraction_notes = extraction_result.get('notes', '')
            
            # Store document type detection results
            doc_obj.detected_document_type = extraction_result.get('detected_document_type', '')
            doc_obj.document_type_confidence = extraction_result.get('document_type_confidence', 0)
            doc_obj.document_type_match = extraction_result.get('document_type_matches_user_selection', True)
            doc_obj.document_type_mismatch_reason = extraction_result.get('detected_vs_user_selection', '')
            
            # Store field completeness data
            field_completeness = extraction_result.get('field_completeness', {})
            doc_obj.field_completeness = field_completeness
            doc_obj.fields_complete_percentage = field_completeness.get('percentage_complete', 0)
            doc_obj.missing_fields = field_completeness.get('missing_fields', [])
            
            # Store agent review flag and reason
            doc_obj.agent_review_required = extraction_result.get('agent_review_required', False)
            doc_obj.agent_review_reason = extraction_result.get('agent_review_reason', '')
            
            # Run validation logic
            validation = ExtractionService.validate_extracted_data(extraction_result)
            
            doc_obj.clarity_flag = validation['clarity_flag']
            doc_obj.validity_flag = validation['validity_flag']
            doc_obj.confidence_score = validation['confidence_score']
            doc_obj.needs_manual_review = validation['needs_manual_review']
            doc_obj.all_fields_present = validation['all_fields_present']
            
            # Extract date fields
            if extracted_fields.get('date_issued'):
                try:
                    from datetime import datetime
                    doc_obj.extracted_date = datetime.fromisoformat(extracted_fields['date_issued']).date()
                except:
                    pass
            
            if extracted_fields.get('date_expiry'):
                try:
                    from datetime import datetime
                    expiry = datetime.fromisoformat(extracted_fields['date_expiry']).date()
                    doc_obj.expiry_date = expiry
                    doc_obj.is_expired = expiry < timezone.now().date()
                except:
                    pass
            
            # Update status based on extraction results
            if validation['needs_manual_review']:
                doc_obj.status = VerificationDocument.DocumentStatus.EXTRACTED
            elif validity.get('is_valid') and not validity.get('is_expired'):
                doc_obj.status = VerificationDocument.DocumentStatus.VERIFIED
            else:
                doc_obj.status = VerificationDocument.DocumentStatus.UPLOADED
            
            doc_obj.extraction_status = 'success'
            doc_obj.extracted_at = timezone.now()
        else:
            # Extraction failed
            doc_obj.extraction_status = 'failed'
            doc_obj.extraction_error = extraction_result.get('error', 'Unknown extraction error')
            doc_obj.status = VerificationDocument.DocumentStatus.UPLOADED
            doc_obj.needs_manual_review = True
        
        doc_obj.save()
        
        # Return response with extraction results
        return Response(
            {
                'document_key': doc_obj.document_key,
                'status': doc_obj.status,
                'extraction_status': doc_obj.extraction_status,
                'file_name': doc_obj.file_name,
                'file_size': doc_obj.file_size,
                'extracted_fields': doc_obj.extracted_fields,
                'clarity_flag': doc_obj.clarity_flag,
                'validity_flag': doc_obj.validity_flag,
                'confidence_score': doc_obj.confidence_score,
                'extraction_notes': doc_obj.extraction_notes,
                'operator_notes': doc_obj.operator_notes,
                'needs_manual_review': doc_obj.needs_manual_review,
                'all_fields_present': doc_obj.all_fields_present,
                'expiry_date': doc_obj.expiry_date.isoformat() if doc_obj.expiry_date else None,
                'is_expired': doc_obj.is_expired,
                'uploaded_at': doc_obj.uploaded_at.isoformat() if doc_obj.uploaded_at else None,
                'extracted_at': doc_obj.extracted_at.isoformat() if doc_obj.extracted_at else None,
                'extraction_error': doc_obj.extraction_error,
            },
            status=status.HTTP_201_CREATED,
        )