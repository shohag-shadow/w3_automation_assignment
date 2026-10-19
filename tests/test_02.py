import random
import pytest
from playwright.sync_api import Page, expect

def test_02(page: Page):
    """Validates that randomly selected books properly load their respective details page.

    Steps:
        1. Navigate to the sandbox homepage.
        2. Identify all rendered product cards.
        3. Randomly select 5 unique book index entries.
        4. For each selection: capture the display title, navigate to its product 
           profile, assert the matching top-level H1 header, ensure the spec grid 
           is visible, and navigate back home.
    """
    target_url = "https://books.toscrape.com/index.html"
    response=page.goto(target_url)

    #page actually loding or not
    assert response is not None, "Failed to load the page entirely."
    assert response.status == 200, f"Expected status 200, but got {response.status}"

    #does home page have atleast 5 books?
    book_locator = page.locator("article.product_pod")
    expect(book_locator.first).to_be_visible()
    total_books = book_locator.count()
    assert total_books >= 5, f"Expected at least 5 books on the homepage, found {total_books}"
    random_indexes = random.sample(range(total_books), 5)

    #random book test
    for index in random_indexes:
        expect(page).to_have_url(target_url)
        current_book = page.locator("article.product_pod").nth(index)
        title_element = current_book.locator("h3 a")
        book_title = title_element.get_attribute("title")
        if not book_title:
            book_title = title_element.inner_text().strip()
            
        title_element.click()
        expect(page).not_to_have_url(target_url)
        page_h1 = page.locator("h1")
        expect(page_h1).to_be_visible()
        expect(page_h1).to_have_text(book_title)
        product_info_table = page.locator("table.table-striped")
        expect(product_info_table).to_be_visible()
        page.go_back()
        expect(book_locator.first).to_be_visible()