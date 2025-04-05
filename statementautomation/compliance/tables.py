import django_tables2 as tables
from .models import Report
from django.urls import reverse

class ReportTable(tables.Table):
    product = tables.Column(linkify=lambda record: reverse('compliance:report_detail', args=[record.pk]))
    portfolio = tables.Column()
    compliance_status = tables.Column()
    date_report_ran = tables.DateColumn()

    class Meta:
        model = Report
        template_name = "django_tables2/bootstrap4.html"
        fields = ("product", "portfolio", "compliance_status", "date_report_ran")
        order_by = ['product']  # Default ordering by product

    def render_product(self, value):
        return value  # Customize rendering if needed

    def render_portfolio(self, value):
        return value  # Customize rendering if needed

    def render_compliance_status(self, value):
        return value  # Customize rendering if needed

    def render_date_report_ran(self, value):
        return value  # Customize rendering if needed
