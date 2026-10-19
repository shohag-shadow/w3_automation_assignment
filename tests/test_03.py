import random
import pytest
from playwright.sync_api import Page, expect

def test_03(page: Page):
    """Verifies that book titles and prices stay consistent between the homepage and detail pages.

    This test samples random products from the Books to Scrape homepage, opens each
    product's detail page, and cross-checks the listing data against the detail data
    to ensure the catalog presents the same information in both places.

    Validation steps include:
        1. Confirms the product grid is loaded and the first book card is visible.
        2. Asserts at least five book cards are available for sampling.
        3. Randomly selects five distinct book cards from the homepage.
        4. Opens each selected book and confirms the detail page heading contains
           the homepage title (trailing dots from truncated titles are ignored).
        5. Confirms the detail page price matches the homepage price exactly.
        6. Navigates back and confirms the product grid is restored.

    Args:
        page (Page): The standard Playwright sync page fixture context injected by pytest.

    Raises:
        AssertionError: If fewer than five books are listed, or if a title or price
            differs between the homepage and the detail page.
    """
    target_url = "https://books.toscrape.com/index.html"
    page.goto(target_url)

    book_cards = page.locator("article.product_pod")
    expect(book_cards.first).to_be_visible()

    total_books = book_cards.count()
    assert total_books >= 5, f"Expected 5+ books, found {total_books}"

    random_indexes = random.sample(range(total_books), 5)

    for index in random_indexes:
        card = book_cards.nth(index)
        title_element = card.locator("h3 a")
        homepage_title = title_element.inner_text().strip(" .")
        homepage_price = card.locator("p.price_color").inner_text().strip()
        title_element.click()
        details_page_h1 = page.locator("h1").first
        details_page_price = page.locator("h1 + p").first
        assert homepage_title in details_page_h1.inner_text(),"titles dont match between home and details page"
        expect(details_page_price).to_have_text(homepage_price)
        page.go_back()
        expect(book_cards.first).to_be_visible()