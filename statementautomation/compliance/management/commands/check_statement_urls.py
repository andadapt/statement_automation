from django.core.management.base import BaseCommand
from compliance.models import Product
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException, Timeout, ConnectionError, InvalidURL
import logging


class Command(BaseCommand):
    help = "Checks statement_url of all products and updates statement_url_status accordingly."

    def add_arguments(self, parser):
        parser.add_argument(
            '--missing',
            action='store_true',
            help='Set all statement_url_status fields to "missing" for testing purposes.'
        )

    def handle(self, *args, **options):
        if options['missing']:
            self.stdout.write("🔧 Setting all statement_url_status fields to 'missing'...\n")
            updated = Product.objects.all().update(statement_url_status='missing')
            self.stdout.write(self.style.SUCCESS(f"✅ Set status to 'missing' for {updated} products."))
            return

        products = Product.objects.all()
        total = products.count()
        self.stdout.write(f"🔍 Checking statement URLs for {total} products...\n")

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
        inputs = soup.find_all('input')
        login_keywords = ['username', 'password', 'login', 'user', 'email']

        for input_ in inputs:
            name = input_.get('name', '').lower()
            input_type = input_.get('type', '').lower()
            if any(keyword in name for keyword in login_keywords) or input_type == 'password':
                return True

        login_text_matches = soup.find_all(text=lambda t: t and 'login' in t.lower())
        return bool(login_text_matches)
