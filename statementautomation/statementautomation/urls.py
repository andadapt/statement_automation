from django.contrib import admin
from django.urls import path, include  # Don't forget to import include
from . import views  # Import views from the current project folder
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('compliance/', include('compliance.urls')),  # Prefix compliance URLs with 'compliance/'
    path('', views.index, name='index'),  # Index page for the whole project
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
 
 