import django_filters
from .models import Report, Portfolio, Product

class ReportFilter(django_filters.FilterSet):
    portfolio = django_filters.ModelChoiceFilter(queryset=Portfolio.objects.all(), empty_label="All Portfolios", label="Portfolio")
    product = django_filters.ModelChoiceFilter(queryset=Product.objects.all(), empty_label="All Products", label="Product")
    date_report_ran = django_filters.DateFromToRangeFilter(label="Date Report Ran")
    compliance_status = django_filters.CharFilter(lookup_expr='icontains', label="Compliance Status")

    class Meta:
        model = Report
        fields = ['portfolio', 'product', 'date_report_ran', 'compliance_status']


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label="Product Name")
    portfolio = django_filters.ModelChoiceFilter(queryset=Portfolio.objects.all(), label="Portfolio")
    product_url = django_filters.CharFilter(lookup_expr='icontains', label="Product URL")
    statement_url = django_filters.CharFilter(lookup_expr='icontains', label="Statement URL")
    product_owner_name = django_filters.CharFilter(lookup_expr='icontains', label="Owner Name")
    product_owner_email = django_filters.CharFilter(lookup_expr='icontains', label="Owner Email")
    statement_url_status = django_filters.ChoiceFilter(choices=Product.URL_STATUS_CHOICES, label="Statement URL Status")

    class Meta:
        model = Product
        exclude = ('comments',)
 