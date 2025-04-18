from django.urls import path
from .views import ReportListView, ReportDetailView, ProductListView  # Import views
from . import views

app_name = 'compliance'  # Namespace for the 'compliance' app

urlpatterns = [
    # Report views
    path('reports/', ReportListView.as_view(), name='report_list'),
    path('reports/<int:pk>/', ReportDetailView.as_view(), name='report_detail'),
    
    # All products (with filtering and table)
    path("products/", ProductListView.as_view(), name="all_products"),
    
    # Products filtered by portfolio
    path("products/<int:portfolio_id>/", views.product_list, name="product_list"),
    
    # Export Products in different formats
    path("products/export/<str:format>/", views.export_products, name="product_export"),
    
    # Portfolio List View
    path("portfolios/", views.portfolio_list, name="portfolio_list"),

    #tools for checking
    path('run-url-check/', views.run_url_check, name='run_url_check'),
    
    path('url-check-report/', views.get_url_check_report, name='url_check_report'),
]
