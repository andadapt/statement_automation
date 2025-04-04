
from django.urls import path
from .views import ReportListView, ReportDetailView  # Ensure ReportListView is imported
app_name = 'compliance'  # This defines the namespace for the 'compliance' app

urlpatterns = [
    path('reports/', ReportListView.as_view(), name='report_list'),
    path('reports/<int:pk>/', ReportDetailView.as_view(), name='report_detail'),
]
