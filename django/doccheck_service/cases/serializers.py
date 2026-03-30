from __future__ import annotations

from typing import List

from rest_framework import serializers

from .models import VerificationCase, VerificationDocument


class SellerSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    phone = serializers.CharField(max_length=32, required=False, allow_blank=True)
    nif = serializers.CharField(max_length=64, required=False, allow_blank=True)


class VerificationCaseCreateSerializer(serializers.Serializer):
    rezerva_reference_id = serializers.CharField(max_length=64)
    seller_info = SellerSerializer(required=False, allow_null=True)  # For frontend
    seller = SellerSerializer(required=False, allow_null=True)  # For API clients
    callback_url = serializers.URLField(required=False, allow_blank=True)
    required_documents = serializers.ListField(
        child=serializers.CharField(max_length=128),
        required=False,
        default=list,
    )
    assessment_data = serializers.JSONField(required=False, default=dict)

    def validate(self, data: dict) -> dict:
        # Support both seller_info (frontend) and seller (API clients)
        seller_data = data.get('seller_info') or data.get('seller')
        if not seller_data:
            raise serializers.ValidationError('seller_info or seller is required')
        data['seller'] = seller_data
        
        # callback_url is optional for frontend submissions
        if 'callback_url' not in data or not data['callback_url']:
            data['callback_url'] = 'https://webhook.doccheck.local/default'
        
        return data

    def validate_rezerva_reference_id(self, value: str) -> str:
        if VerificationCase.objects.filter(rezerva_reference_id=value).exists():
            raise serializers.ValidationError('rezerva_reference_id already processed')
        return value


class VerificationCaseResponseSerializer(serializers.ModelSerializer):
    upload_url = serializers.SerializerMethodField()

    class Meta:
        model = VerificationCase
        fields = (
            'provider_case_id',
            'upload_url',
            'status',
            'expires_at',
        )

    def get_upload_url(self, obj: VerificationCase) -> str:
        base = self.context.get('upload_base', 'https://app.doccheck.local/upload')
        return f"{base}/{obj.provider_case_id}?token={obj.upload_token}"


class DocumentStatusSerializer(serializers.Serializer):
    document_key = serializers.CharField(max_length=128)
    status = serializers.ChoiceField(choices=VerificationDocument.DocumentStatus.choices)
    reason = serializers.CharField(max_length=255, required=False, allow_blank=True)


class CaseStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=VerificationCase.CaseStatus.choices)
    documents = DocumentStatusSerializer(many=True, required=False)
    overall_reason = serializers.CharField(max_length=255, required=False, allow_blank=True)


class VerificationDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationDocument
        fields = (
            'document_key',
            'status',
            'extraction_status',
            'user_submitted_document_type',
            'detected_document_type',
            'document_type_confidence',
            'document_type_match',
            'document_type_mismatch_reason',
            'extracted_fields',
            'field_completeness',
            'fields_complete_percentage',
            'missing_fields',
            'clarity_flag',
            'clarity_assessment',
            'validity_flag',
            'validity_assessment',
            'confidence_score',
            'extraction_notes',
            'operator_notes',
            'needs_manual_review',
            'all_fields_present',
            'agent_review_required',
            'agent_review_reason',
            'expiry_date',
            'is_expired',
            'reason',
            'uploaded_at',
            'extracted_at',
            'extraction_error',
            'updated_at',
        )


class VerificationCaseDetailSerializer(serializers.ModelSerializer):
    documents = VerificationDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = VerificationCase
        fields = (
            'provider_case_id',
            'rezerva_reference_id',
            'callback_url',
            'status',
            'seller_name',
            'seller_email',
            'seller_phone',
            'expires_at',
            'metadata',
            'created_at',
            'updated_at',
            'documents',
        )
