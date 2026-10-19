import pytest
from playwright.sync_api import Page, expect


def test_06(page: Page):
    target_url = "https://quotes.toscrape.com/"
    page.goto(target_url)

    login_nav = page.get_by_role("link", name="Login", exact=True)
    expect(login_nav).to_be_visible()
    login_nav.click()

    expect(page).to_have_url("https://quotes.toscrape.com/login")

    # page.locator('input[name="username"]').type("user")
    page.locator('input[name="username"]').press_sequentially("user", delay=500)
    # page.locator('input[name="password"]').type("password")
    page.locator('input[name="password"]').press_sequentially("password", delay=500)
    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url("https://quotes.toscrape.com/")

    logout_link = page.get_by_role("link", name="Logout", exact=True)
    expect(logout_link).to_be_visible()
    expect(logout_link).to_have_attribute("href", "/logout")