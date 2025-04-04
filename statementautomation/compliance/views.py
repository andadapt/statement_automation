from django.shortcuts import render
from django.views.generic import ListView
from .models import Report


class ReportListView(ListView):
    model = Report
    template_name = 'report_list.html'  # Template to render
    context_object_name = 'reports'  # Variable to access in the template
    paginate_by = 10  # Optional: 10 reports per page (you can remove this if you don't want pagination)
    
    # Set default ordering to product name alphabetically
    ordering = ['product__name']
