import pytest
from playwright.sync_api import Page, expect

def test_01(page: Page):
    target_url = "https://books.toscrape.com/index.html"
    response = page.goto(target_url)
    
    #page actually loding or not
    assert response is not None, "Failed to load the page entirely."
    assert response.status == 200, f"Expected status 200, but got {response.status}"

    #is url right?
    assert target_url in response.url

    #is title right?
    expect(page).to_have_title("All products | Books to Scrape - Sandbox")

    #heading test
    visible_headings = page.locator("h1, h2, h3, h4, h5, h6").all()
    assert len(visible_headings) > 0, "No visible headings (h1-h6) were found on the page."
    
    for header in visible_headings:
        expect(header).to_be_visible()
        text = header.inner_text().strip()
        assert len(text) > 0, f"Found an empty heading element: {header}"

    #book section test
    book_section = page.locator("section").all()
    assert len(book_section)==1 ,"There is more than one section in this page"
    expect(book_section[0]).to_be_visible()
