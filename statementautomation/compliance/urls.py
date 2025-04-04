
from django.urls import path
from .views import ReportListView
app_name = 'compliance'  # This defines the namespace for the 'compliance' app

urlpatterns = [
    path('reports/', ReportListView.as_view(), name='report_list'),
]
