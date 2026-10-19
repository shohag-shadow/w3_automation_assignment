import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser_instance = p.chromium.launch(headless=False)
        yield browser_instance
        browser_instance.close()

@pytest.fixture(scope="function") 
def page(browser):
    context = browser.new_context()
    
    page_instance = context.new_page()
    yield page_instance
    page_instance.close()
    context.close()