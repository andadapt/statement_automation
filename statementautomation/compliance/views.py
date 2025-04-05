from django.shortcuts import render
from django.views.generic import ListView
import django_filters
from .models import Report, Portfolio, Product  # <-- Make sure Portfolio and Product are imported
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from .models import Product
from simple_history.utils import update_change_reason
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from .models import Report
from .filters import ReportFilter
from compliance.filters import ReportFilter  # now this works
from .tables import ReportTable


class ReportListView(SingleTableMixin, FilterView):
    model = Report
    table_class = ReportTable
    template_name = "compliance/report_list.html"
    context_object_name = "reports"
    filterset_class = ReportFilter
    paginate_by = 10

class ReportDetailView(DetailView):
    model = Report
    template_name = 'compliance/report_detail.html'
    context_object_name = 'report'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report = self.get_object()
        context['history'] = report.history.all()
        return context