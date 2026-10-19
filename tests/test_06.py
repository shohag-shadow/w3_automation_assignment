import pytest
from playwright.sync_api import Page, expect


def test_06(page: Page):
    """Verifies the login flow on the Quotes to Scrape sandbox site.

    This test performs an end-to-end login using the demo credentials and checks
    that the interface reflects an authenticated session afterwards.

    Validation steps include:
        1. Confirms the Login link is visible on the homepage and clicks it.
        2. Asserts the browser lands on the login page URL.
        3. Types the username and password character by character with a delay
           to simulate real keyboard input.
        4. Submits the form and asserts the user is redirected to the homepage.
        5. Confirms the Logout link is visible and points to "/logout",
           indicating a successful login.

    Args:
        page (Page): The standard Playwright sync page fixture context injected by pytest.

    Raises:
        AssertionError: If the Login link is missing, a URL redirect is incorrect,
            or the Logout link is not shown with the expected href after login.
    """
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