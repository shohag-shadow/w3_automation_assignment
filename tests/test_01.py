import pytest
from playwright.sync_api import Page, expect

def test_01(page: Page):
    target_url = "https://books.toscrape.com/index.html"
    response = page.goto(target_url)
    
    assert response is not None, "Failed to load the page entirely."
    assert response.status == 200, f"Expected status 200, but got {response.status}"
    assert target_url in response.url
    
    expect(page).to_have_title("All products | Books to Scrape - Sandbox")
    

