from import_export import resources
from .models import Product

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        exclude = ['comments']  # Optional: Exclude if you don't want this exported
