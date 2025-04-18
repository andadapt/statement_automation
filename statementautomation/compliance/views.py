from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from threading import Thread
from django.views.generic import ListView, DetailView
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from django.http import HttpResponse
from django_tables2 import RequestConfig
from .services.url_checker import check_statement_url
from .models import Report, Portfolio, Product
from .filters import ReportFilter, ProductFilter
from .tables import ReportTable, ProductTable, PortfolioTable
from .resources import ProductResource
from import_export.formats.base_formats import CSV, XLSX
from simple_history.utils import update_change_reason
from django.contrib import messages
import time
from django.core.cache import cache
from threading import Thread
from time import time

# View for listing reports
class ReportListView(SingleTableMixin, FilterView):
    model = Report
    table_class = ReportTable
    template_name = "compliance/report_list.html"
    context_object_name = "reports"
    filterset_class = ReportFilter
    paginate_by = 10


# View for showing report details
class ReportDetailView(DetailView):
    model = Report
    template_name = 'compliance/report_detail.html'
    context_object_name = 'report'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report = self.get_object()
        context['history'] = report.history.all()
        return context


# View for listing all products with filters
class ProductListView(SingleTableMixin, FilterView):
    model = Product
    table_class = ProductTable
    template_name = "compliance/product_list.html"
    filterset_class = ProductFilter
    paginate_by = 20


# Export products (filtered) in CSV or XLSX
def export_products(request, format):
    resource = ProductResource()
    f = ProductFilter(request.GET, queryset=resource._meta.model.objects.all())
    dataset = resource.export(f.qs)

    if format == 'csv':
        file_format = CSV()
        content_type = 'text/csv'
        extension = 'csv'
    elif format == 'xlsx':
        file_format = XLSX()
        content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        extension = 'xlsx'
    else:
        return HttpResponse("Unsupported format", status=400)

    export_data = file_format.export_data(dataset)
    response = HttpResponse(export_data, content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename=products.{extension}'
    return response


# View to list all portfolios with clickable names to product lists
def portfolio_list(request):
    portfolios = Portfolio.objects.all()
    table = PortfolioTable(portfolios)
    RequestConfig(request).configure(table)
    return render(request, "compliance/portfolio_list.html", {
        'table': table
    })


# View to list all products within a specific portfolio
def product_list(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
    products = Product.objects.filter(portfolio=portfolio)
    table = ProductTable(products)
    RequestConfig(request).configure(table)
    return render(request, "compliance/product_list.html", {
        'table': table,
        'portfolio': portfolio
    })


class ProductListView(SingleTableMixin, FilterView):
    model = Product
    table_class = ProductTable
    template_name = "compliance/product_list.html"
    filterset_class = ProductFilter
    paginate_by = 10

# url checking code, using a simple temp store for results
def run_url_check_task(user_id):
    start = time()

    result = {
        'working': 0,
        'broken': 0,
        'missing': 0,
        'authentication': 0,
        'total': 0,
        'updated': 0,
        'duration': 0.0
    }

    for product in Product.objects.all():
        new_status = check_statement_url(product)
        if product.statement_url_status != new_status:
            product.statement_url_status = new_status
            product.save(update_fields=["statement_url_status"])
            result['updated'] += 1

        result['total'] += 1
        result[new_status] += 1

    result['duration'] = round(time() - start, 2)
    cache.set(f"url_check_report_{user_id}", result, timeout=300)

def run_url_check(request):
    if request.method == 'POST':
        user_id = str(request.user.id or 'anonymous')
        thread = Thread(target=run_url_check_task, args=(user_id,))
        thread.start()

        return JsonResponse({'status': 'URL check started. This may take a moment.'})

    return render(request, 'compliance/progress.html')

def get_url_check_report(request):
    user_id = str(request.user.id or 'anonymous')
    report = cache.get(f"url_check_report_{user_id}")
    if report:
        return JsonResponse({'done': True, 'report': report})
    else:
        return JsonResponse({'done': False})