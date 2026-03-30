from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0002_add_ai_extraction'),
    ]

    operations = [
        # Document Type Detection fields
        migrations.AddField(
            model_name='verificationdocument',
            name='user_submitted_document_type',
            field=models.CharField(
                blank=True,
                max_length=128,
                help_text='Document type selected by user (may differ from AI detection)',
            ),
        ),
        migrations.AddField(
            model_name='verificationdocument',
            name='detected_document_type',
            field=models.CharField(
                blank=True,
                max_length=128,
                help_text='Document type detected by AI from visual content',
            ),
        ),
        migrations.AddField(
            model_name='verificationdocument',
            name='document_type_confidence',
            field=models.IntegerField(
                default=0,
                help_text='AI confidence in document type detection (0-100)',
            ),
        ),
        migrations.AddField(
            model_name='verificationdocument',
            name='document_type_match',
            field=models.BooleanField(
                default=True,
                help_text='True if AI detection matches user selection',
            ),
        ),
        migrations.AddField(
            model_name='verificationdocument',
            name='document_type_mismatch_reason',
            field=models.TextField(
                blank=True,
                help_text='Reason if detected type differs from user selection',
            ),
        ),
        
        # Field Completeness Tracking
        migrations.AddField(
            model_name='verificationdocument',
            name='field_completeness',
            field=models.JSONField(
                blank=True,
                default=dict,
                help_text='{ total_expected_fields, fields_found, missing_fields, percentage_complete }',
            ),
        ),
        migrations.AddField(
            model_name='verificationdocument',
            name='fields_complete_percentage',
            field=models.IntegerField(
                default=0,
                help_text='Percentage of expected fields that were found (0-100)',
            ),
        ),
        migrations.AddField(
            model_name='verificationdocument',
            name='missing_fields',
            field=models.JSONField(
                blank=True,
                default=list,
                help_text='List of expected fields that are missing',
            ),
        ),
        
        # Agent Review fields
        migrations.AddField(
            model_name='verificationdocument',
            name='agent_review_required',
            field=models.BooleanField(
                default=False,
                help_text='True if AI flagged document for mandatory agent review (type mismatch, incomplete fields, unclear)',
            ),
        ),
        migrations.AddField(
            model_name='verificationdocument',
            name='agent_review_reason',
            field=models.TextField(
                blank=True,
                help_text='Reason why agent review is required',
            ),
        ),
        
        # Update extracted_fields help text
        migrations.AlterField(
            model_name='verificationdocument',
            name='extracted_fields',
            field=models.JSONField(
                blank=True,
                default=dict,
                help_text='{ name, nif, date_issued, date_expiry, issuer, reference_number, property_reference, condominium, unit_number }',
            ),
        ),
    ]
