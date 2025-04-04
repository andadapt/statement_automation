from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin  # Use ImportExportModelAdmin

from .models import Portfolio, Product, Report

# Create a Resource class for Product model (handles import/export functionality)
class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ('id', 'name', 'portfolio', 'product_url', 'statement_url')
        export_order = ('id', 'name', 'portfolio', 'product_url', 'statement_url')

# Create a Resource class for Report model (handles import/export functionality)
class ReportResource(resources.ModelResource):
    class Meta:
        model = Report
        fields = ('id', 'product', 'portfolio', 'prepared_by_date', 'last_reviewed_date', 'last_tested_date', 'days_since_last_tested', 'tested_by', 'compliance_status', 'wcag', 'date_report_ran')
        export_order = ('id', 'product', 'portfolio', 'prepared_by_date', 'last_reviewed_date', 'last_tested_date', 'days_since_last_tested', 'tested_by', 'compliance_status', 'wcag', 'date_report_ran')

# Register Product model with Import/Export functionality
@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):  # Using ImportExportModelAdmin
    resource_classes = [ProductResource]
    list_display = ('name', 'portfolio', 'product_url', 'statement_url')
    search_fields = ('name', 'portfolio__name')
    list_filter = ('portfolio',)

# Register Report model with Import/Export and Simple History functionality
@admin.register(Report)
class ReportAdmin(SimpleHistoryAdmin, ImportExportModelAdmin, admin.ModelAdmin):  # Using ImportExportModelAdmin
    resource_classes = [ReportResource]
    list_display = ('product', 'portfolio', 'prepared_by_date', 'last_reviewed_date', 'date_report_ran', 'compliance_status')
    search_fields = ('product__name', 'portfolio__name', 'date_report_ran')
    history_list_display = ('history_user', 'history_date', 'history_type')  # Show historical changes
    list_filter = ('product', 'portfolio', 'compliance_status')

# Optionally, register Portfolio model if necessary
admin.site.register(Portfolio)
