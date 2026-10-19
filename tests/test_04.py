import requests
from urllib.parse import urljoin
from playwright.sync_api import Page


def test_04(page: Page):
    """Verifies that every link on the Books to Scrape homepage is valid and reachable.

    This test collects all anchor elements from the homepage and requests each
    destination over HTTP to catch missing or broken links before users find them.

    Validation steps include:
        1. Collects every anchor element present on the homepage.
        2. Asserts each anchor has a non-empty href attribute.
        3. Resolves relative hrefs into absolute URLs using the current page URL.
        4. Sends a GET request for each URL through a shared requests session.
        5. Confirms every destination responds with HTTP 200 OK.

    Args:
        page (Page): The standard Playwright sync page fixture context injected by pytest.

    Raises:
        AssertionError: If an anchor has no href, or if any linked URL returns a
            status code other than 200.
    """
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