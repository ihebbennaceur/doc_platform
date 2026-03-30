from __future__ import annotations

import uuid
from typing import Any

from django.db import models
from django.utils import timezone


class VerificationCase(models.Model):
    class CaseStatus(models.TextChoices):
        CREATED = 'created', 'Created'
        IN_REVIEW = 'in_review', 'In Review'
        VERIFIED = 'verified', 'Verified'
        REJECTED = 'rejected', 'Rejected'

    provider_case_id = models.CharField(
        primary_key=True,
        max_length=32,
        editable=False,
        unique=True,
    )
    rezerva_reference_id = models.CharField(max_length=64, unique=True)
    callback_url = models.URLField()
    status = models.CharField(max_length=20, choices=CaseStatus.choices, default=CaseStatus.CREATED)
    seller_name = models.CharField(max_length=255)
    seller_email = models.EmailField()
    seller_phone = models.CharField(max_length=32)
    upload_token = models.CharField(max_length=64, default='', blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.provider_case_id:
            self.provider_case_id = generate_case_id()
        if not self.upload_token:
            self.upload_token = uuid.uuid4().hex
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(days=7)
        super().save(*args, **kwargs)

    def __str__(self) -> str:  # pragma: no cover
        return f"DocCheckCase<{self.provider_case_id}>"


class VerificationDocument(models.Model):
    class DocumentStatus(models.TextChoices):
        PENDING = 'pending', 'Pending Upload'
        PROCESSING = 'processing', 'Processing (AI extraction)'
        UPLOADED = 'uploaded', 'Uploaded'
        EXTRACTED = 'extracted', 'Extracted (awaiting review)'
        VERIFIED = 'verified', 'Verified'
        EXPIRED = 'expired', 'Expired'
        REJECTED = 'rejected', 'Rejected'

    class ClarityFlag(models.TextChoices):
        CLEAR = 'CLEAR', 'Document is clear and legible'
        PARTIAL = 'PARTIAL', 'Document is partially clear'
        UNCLEAR = 'UNCLEAR', 'Document is unclear or incomplete'
        NOT_ASSESSED = 'NOT_ASSESSED', 'Not yet assessed'

    class ValidityFlag(models.TextChoices):
        VALID = 'VALID', 'Document is valid'
        EXPIRED = 'EXPIRED', 'Document is expired'
        INVALID = 'INVALID', 'Document is invalid'
        NOT_ASSESSED = 'NOT_ASSESSED', 'Not yet assessed'

    provider_case = models.ForeignKey(VerificationCase, related_name='documents', on_delete=models.CASCADE)
    document_key = models.CharField(max_length=128)
    status = models.CharField(max_length=32, choices=DocumentStatus.choices, default=DocumentStatus.PENDING)
    
    # File metadata & storage
    file_path = models.CharField(max_length=255, blank=True)  # S3 key or local path: media/cases/{case_id}/{doc_key}/{filename}
    file_name = models.CharField(max_length=255, blank=True)
    file_size = models.IntegerField(default=0)
    mime_type = models.CharField(max_length=50, blank=True)
    
    # AI Extraction results
    extraction_status = models.CharField(
        max_length=32,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('success', 'Success'),
            ('failed', 'Failed'),
        ],
        default='pending',
    )
    
    # Document Type Detection
    user_submitted_document_type = models.CharField(
        max_length=128,
        blank=True,
        help_text='Document type selected by user (may differ from AI detection)',
    )
    detected_document_type = models.CharField(
        max_length=128,
        blank=True,
        help_text='Document type detected by AI from visual content',
    )
    document_type_confidence = models.IntegerField(
        default=0,
        help_text='AI confidence in document type detection (0-100)',
    )
    document_type_match = models.BooleanField(
        default=True,
        help_text='True if AI detection matches user selection',
    )
    document_type_mismatch_reason = models.TextField(
        blank=True,
        help_text='Reason if detected type differs from user selection',
    )
    
    extracted_fields = models.JSONField(
        default=dict,
        blank=True,
        help_text='{ name, nif, date_issued, date_expiry, issuer, reference_number, property_reference, condominium, unit_number }',
    )
    
    # Field Completeness Tracking
    field_completeness = models.JSONField(
        default=dict,
        blank=True,
        help_text='{ total_expected_fields, fields_found, missing_fields, percentage_complete }',
    )
    fields_complete_percentage = models.IntegerField(
        default=0,
        help_text='Percentage of expected fields that were found (0-100)',
    )
    missing_fields = models.JSONField(
        default=list,
        blank=True,
        help_text='List of expected fields that are missing',
    )
    
    extracted_date = models.DateField(null=True, blank=True)  # document issue date from extraction
    is_expired = models.BooleanField(default=False)
    expiry_date = models.DateField(null=True, blank=True)  # calculated from extracted_date + validity_months
    
    # AI Assessment scores
    clarity_assessment = models.JSONField(
        default=dict,
        blank=True,
        help_text='{ is_clear, legibility, overall_confidence, issues }',
    )
    clarity_flag = models.CharField(
        max_length=20,
        choices=ClarityFlag.choices,
        default=ClarityFlag.NOT_ASSESSED,
    )
    
    validity_assessment = models.JSONField(
        default=dict,
        blank=True,
        help_text='{ is_valid, is_expired, validity_period_months, concerns }',
    )
    validity_flag = models.CharField(
        max_length=20,
        choices=ValidityFlag.choices,
        default=ValidityFlag.NOT_ASSESSED,
    )
    
    confidence_score = models.IntegerField(default=0, help_text='Overall AI confidence 0-100')
    extraction_notes = models.TextField(blank=True, help_text='AI observations about the document')
    
    # Operator review & manual notes
    operator_notes = models.TextField(blank=True, help_text='Manual notes from operator/agent review')
    needs_manual_review = models.BooleanField(default=False)
    agent_review_required = models.BooleanField(
        default=False,
        help_text='True if AI flagged document for mandatory agent review (type mismatch, incomplete fields, unclear)',
    )
    agent_review_reason = models.TextField(
        blank=True,
        help_text='Reason why agent review is required',
    )
    all_fields_present = models.BooleanField(default=False)
    
    extraction_error = models.TextField(blank=True, help_text='Error message if extraction failed')
    
    reason = models.CharField(max_length=255, blank=True)  # rejection reason
    uploaded_at = models.DateTimeField(null=True, blank=True)
    extracted_at = models.DateTimeField(null=True, blank=True)  # when AI extraction completed
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('provider_case', 'document_key')
        ordering = ['document_key', '-uploaded_at']

    def __str__(self) -> str:  # pragma: no cover
        return f"Doc<{self.document_key}>={self.status}/{self.extraction_status}"


class DocumentValidity(models.Model):
    """Reference table for document types and validity rules"""
    
    document_key = models.CharField(max_length=128, unique=True, primary_key=True)
    name = models.CharField(max_length=255)  # 'Caderneta Predial Urbana'
    validity_months = models.IntegerField(null=True, blank=True)  # 12, 6, 10*12, None (no expiry)
    cost_min = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cost_max = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    issuer = models.CharField(max_length=255)  # 'Finanças', 'IRN', 'ADENE', etc.
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Document Validities'
    
    def __str__(self) -> str:
        return f"{self.name} ({self.validity_months} months)" if self.validity_months else self.name


class WebhookEvent(models.Model):
    provider_case = models.ForeignKey(VerificationCase, related_name='webhook_events', on_delete=models.CASCADE)
    event_id = models.CharField(max_length=50, unique=True)
    payload_json = models.JSONField()
    delivery_status = models.CharField(max_length=32, default='pending')
    attempt_count = models.IntegerField(default=0)
    last_attempt_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.event_id


def generate_case_id() -> str:
    """Return stable provider case id."""
    return f"dc_case_{uuid.uuid4().hex[:8]}"
