import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html
from .models import Report, Product, Portfolio

class ReportTable(tables.Table):
    product = tables.Column(linkify=lambda record: reverse('compliance:report_detail', args=[record.pk]))
    portfolio = tables.Column()
    compliance_status = tables.Column()
    date_report_ran = tables.DateColumn()

    class Meta:
        model = Report
        template_name = "django_tables2/bootstrap4.html"
        fields = ("product", "portfolio", "compliance_status", "date_report_ran")
        order_by = ['product']

    def render_product(self, value):
        return value

    def render_portfolio(self, value):
        return value

    def render_compliance_status(self, value):
        return value

    def render_date_report_ran(self, value):
        return value

class ProductTable(tables.Table):
    name = tables.Column(verbose_name="Product", accessor="name")
    portfolio = tables.Column()
    product_url = tables.Column()
    statement_url = tables.Column()
    product_owner_name = tables.Column()
    product_owner_email = tables.Column()
    statement_url_status = tables.Column()

    class Meta:
        model = Product
        template_name = "django_tables2/bootstrap4.html"
        exclude = ("comments",)

    def render_name(self, value, record):
        if record.reports.exists():
            url = reverse('compliance:report_detail', args=[record.reports.last().pk])
            return format_html('<a href="{}">{}</a>', url, value)
        return value

    def render_product_owner_email(self, value):
        if value:
            return format_html('<a href="mailto:{}">{}</a>', value, value)
        return "-"

    def render_product_url(self, value):
        if value:
            return format_html('<a href="{}" target="_blank">{}</a>', value, value)
        return "-"

    def render_statement_url(self, value):
        if value:
            return format_html('<a href="{}" target="_blank">{}</a>', value, value)
        return "-"

class PortfolioTable(tables.Table):
    name = tables.Column(verbose_name="Portfolio")

    def render_name(self, value, record):
        url = reverse("compliance:product_list", args=[record.id])
        return format_html('<a href="{}">{}</a>', url, value)

    description = tables.Column(verbose_name="Comments")

    class Meta:
        model = Portfolio
        template_name = "django_tables2/bootstrap4.html"
        fields = ("name", "description")
