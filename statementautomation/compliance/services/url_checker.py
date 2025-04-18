import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException, Timeout, ConnectionError, InvalidURL

def check_statement_url(product):
    url = product.statement_url

    if not url:
        return 'missing'

    try:
        response = requests.get(url, timeout=10, allow_redirects=True)
        content = response.text.lower()

        if response.status_code in (401, 403):
            return 'authentication'

        if response.status_code >= 400:
            return 'broken'

        soup = BeautifulSoup(content, 'html.parser')

        if contains_login_elements(soup):
            return 'authentication'

        if "accessibility statement" in content:
            return 'working'

        return 'broken'

    except (Timeout, ConnectionError, InvalidURL, RequestException):
        return 'broken'
    except Exception:
        return 'broken'

def contains_login_elements(soup):
    inputs = soup.find_all('input')
    login_keywords = ['username', 'password', 'login', 'user', 'email']

    for input_ in inputs:
        name = input_.get('name', '').lower()
        input_type = input_.get('type', '').lower()
        if any(keyword in name for keyword in login_keywords) or input_type == 'password':
            return True

    login_text_matches = soup.find_all(text=lambda t: t and 'login' in t.lower())
    return bool(login_text_matches)
