import requests
from urllib.parse import urljoin
from playwright.sync_api import Page


def test_04(page: Page):
    target_url = "https://books.toscrape.com/index.html"
    page.goto(target_url)
    
    session = requests.Session()
    for anchor in page.locator("a").all():
        href = anchor.get_attribute("href")
        assert href, f"Anchor has no href: {anchor.inner_html()}"
        url = urljoin(page.url, href)
        resp = session.get(url, timeout=10)
        assert resp.status_code == 200, f"Broken link: {url} -> {resp.status_code}"
    session.close()