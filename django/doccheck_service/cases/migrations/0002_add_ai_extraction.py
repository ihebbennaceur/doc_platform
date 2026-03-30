from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0001_initial'),
    ]

    operations = [
        # Add new fields to VerificationDocument
        migrations.AddField(
            model_name='verificationdocument',
            name='extraction_status',
            field=models.CharField(
                choices=[('pending', 'Pending'), ('processing', 'Processing'), ('success', 'Success'), ('failed', 'Failed')],
                default='pending',
                max_length=32,
            ),
        ),
        migrations.AddField(
            model_name='verificationdocument',
            name='extracted_fields',
            field=models.JSONField(blank=True, default=dict, help_text='{ name, date_issued, date_expiry, issuer, reference_number, property_reference }'),
        ),
        migrations.AddField(
            model_name='verificationdocument',
            name='clarity_assessment',
            field=models.JSONField(blank=True, default=dict, help_text='{ is_clear, legibility, overall_confidence, issues }'),
        ),
        migrations.AddField(
            model_name='verificationdocument',
            name='clarity_flag',
            field=models.CharField(
                choices=[('CLEAR', 'Document is clear and legible'), ('PARTIAL', 'Document is partially clear'), ('UNCLEAR', 'Document is unclear or incomplete'), ('NOT_ASSESSED', 'Not yet assessed')],
                default='NOT_ASSESSED',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='verificationdocument',
            name='validity_assessment',
            field=models.JSONField(blank=True, default=dict, help_text='{ is_valid, is_expired, validity_period_months, concerns }'),
        ),
        migrations.AddField(
            model_name='verificationdocument',
            name='validity_flag',
            field=models.CharField(
                choices=[('VALID', 'Document is valid'), ('EXPIRED', 'Document is expired'), ('INVALID', 'Document is invalid'), ('NOT_ASSESSED', 'Not yet assessed')],
                default='NOT_ASSESSED',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='verificationdocument',
            name='confidence_score',
            field=models.IntegerField(default=0, help_text='Overall AI confidence 0-100'),
        ),
        migrations.AddField(
            model_name='verificationdocument',
            name='extraction_notes',
            field=models.TextField(blank=True, help_text='AI observations about the document'),
        ),
        migrations.AddField(
            model_name='verificationdocument',
            name='operator_notes',
            field=models.TextField(blank=True, help_text='Manual notes from operator/agent review'),
        ),
        migrations.AddField(
            model_name='verificationdocument',
            name='needs_manual_review',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='verificationdocument',
            name='all_fields_present',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='verificationdocument',
            name='extraction_error',
            field=models.TextField(blank=True, help_text='Error message if extraction failed'),
        ),
        migrations.AddField(
            model_name='verificationdocument',
            name='extracted_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterModelOptions(
            name='verificationdocument',
            options={'ordering': ['document_key', '-uploaded_at']},
        ),
        migrations.AlterField(
            model_name='verificationdocument',
            name='status',
            field=models.CharField(
                choices=[
                    ('pending', 'Pending Upload'),
                    ('processing', 'Processing (AI extraction)'),
                    ('uploaded', 'Uploaded'),
                    ('extracted', 'Extracted (awaiting review)'),
                    ('verified', 'Verified'),
                    ('expired', 'Expired'),
                    ('rejected', 'Rejected'),
                ],
                default='pending',
                max_length=32,
            ),
        ),
    ]
