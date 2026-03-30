from django.urls import path

from .views import (
	APIRootView,
	CaseStatusUpdateView,
	DocumentUploadView,
	VerificationCaseCreateView,
	VerificationCaseDetailView,
)

app_name = 'cases'

urlpatterns = [
	path('', APIRootView.as_view(), name='api-root'),
	path('cases/', VerificationCaseCreateView.as_view(), name='case-create'),
	path('cases/<str:provider_case_id>/', VerificationCaseDetailView.as_view(), name='case-detail'),
	path(
		'cases/<str:provider_case_id>/status/',
		CaseStatusUpdateView.as_view(),
		name='case-status-update',
	),
	path(
		'cases/<str:provider_case_id>/documents/upload',
		DocumentUploadView.as_view(),
		name='document-upload',
	),
]
