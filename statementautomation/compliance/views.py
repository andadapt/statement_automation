from django.shortcuts import render
from django.views.generic import ListView
import django_filters
from .models import Report, Portfolio, Product  # <-- Make sure Portfolio and Product are imported

# Create a filter class using django-filter for easy filtering
class ReportFilter(django_filters.FilterSet):
    portfolio = django_filters.ModelChoiceFilter(queryset=Portfolio.objects.all(), empty_label="All Portfolios", label="Portfolio")
    product = django_filters.ModelChoiceFilter(queryset=Product.objects.all(), empty_label="All Products", label="Product")
    date_report_ran = django_filters.DateFromToRangeFilter(label="Date Report Ran")
    compliance_status = django_filters.CharFilter(lookup_expr='icontains', label="Compliance Status")

    class Meta:
        model = Report
        fields = ['portfolio', 'product', 'date_report_ran', 'compliance_status']

# Report List View with Filtering and Sorting
class ReportListView(ListView):
    model = Report
    template_name = 'report_list.html'  # Template for displaying reports
    context_object_name = 'reports'
    paginate_by = 10  # Number of reports per page
    
    # Set default ordering to product name
    ordering = ['product__name']

    def get_queryset(self):
        queryset = Report.objects.all()
        filter = ReportFilter(self.request.GET, queryset=queryset)
        return filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ReportFilter(self.request.GET, queryset=self.get_queryset())
        return context
