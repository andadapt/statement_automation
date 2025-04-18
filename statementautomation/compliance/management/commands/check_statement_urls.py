import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from compliance .models import Product
from requests.exceptions import RequestException, Timeout, ConnectionError, InvalidURL
import logging

class Command(BaseCommand):
    help = "Checks statement_url of all products and updates statement_url_status accordingly."

    def handle(self, *args, **kwargs):
        products = Product.objects.all()
        total = products.count()
        self.stdout.write(f"Checking statement URLs for {total} products...\n")

        for idx, product in enumerate(products, start=1):
            status = self.check_statement_url(product)
            if product.statement_url_status != status:
                product.statement_url_status = status
                product.save(update_fields=["statement_url_status"])
            self.stdout.write(f"[{idx}/{total}] {product.name}: {status}")

        self.stdout.write(self.style.SUCCESS("\n✅ Finished checking all products."))

    def check_statement_url(self, product):
        url = product.statement_url

        if not url:
            return 'missing'

        try:
            response = requests.get(url, timeout=10, allow_redirects=True)
            status_code = response.status_code
            content = response.text.lower()

            if status_code in (401, 403):
                return 'authentication'

            if status_code >= 400:
                return 'broken'

            soup = BeautifulSoup(content, 'html.parser')

            if self.contains_login_elements(soup):
                return 'authentication'

            if "accessibility statement" in content:
                return 'working'

            return 'broken'

        except (Timeout, ConnectionError, InvalidURL, RequestException) as e:
            logging.warning(f"Error checking URL for {product.name}: {e}")
            return 'broken'
        except Exception as e:
            logging.error(f"Unexpected error for {product.name}: {e}", exc_info=True)
            return 'broken'

    def contains_login_elements(self, soup):
        """Returns True if page has login fields."""
        inputs = soup.find_all('input')
        login_keywords = ['username', 'password', 'login', 'user', 'email']

        for input_ in inputs:
            name = input_.get('name', '').lower()
            input_type = input_.get('type', '').lower()
            if any(keyword in name for keyword in login_keywords) or input_type == 'password':
                return True

        # Also check for login buttons or links
        login_text_matches = soup.find_all(text=lambda t: t and 'login' in t.lower())
        if login_text_matches:
            return True

        return False
