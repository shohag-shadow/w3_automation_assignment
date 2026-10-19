import random
import pytest
from playwright.sync_api import Page, expect

def test_03(page: Page):
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