import pytest
from playwright.sync_api import Page, expect

def test_05(page: Page):
    target_url = "https://books.toscrape.com/index.html"
    page.goto(target_url)
    
    max_pages = 5
    page_count = 1
    while page_count <= max_pages:
        images = page.locator(".image_container img").all()
        assert len(images) > 0, f"No product images found on page number {page_count}"
        for img in images:
            expect(img).to_be_visible()
            src = img.get_attribute("src")
            assert src and len(src.strip()) > 0, f"Found image with missing or empty 'src'"
            alt = img.get_attribute("alt")
            assert alt and len(alt.strip()) > 0, f"Found image with missing or empty 'alt'"
            img_class = img.get_attribute("class")
            assert img_class and "thumbnail" in img_class, f"Image class '{img_class}' missing 'thumbnail' key"
        next_button = page.get_by_role("link", name="next", exact=True)
        if next_button.is_visible() and page_count < max_pages:
            next_button.click()
            page_count += 1
        else:
            break 