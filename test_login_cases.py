import re
import pytest
from playwright.sync_api import Page, expect

LOGIN_URL = "https://the-internet.herokuapp.com/login"
VALID_USERNAME = "tomsmith"
VALID_PASSWORD = "SuperSecretPassword!"


@pytest.fixture
def login_page(page: Page):
    page.goto(LOGIN_URL)
    return page


def login(page: Page, username: str, password: str):
    page.locator("#username").fill(username)
    page.locator("#password").fill(password)
    page.get_by_role("button", name="Login").click()


def test_01_login_page_loads(login_page):
    expect(login_page).to_have_url(LOGIN_URL)
    expect(login_page).to_have_title("The Internet")
    expect(login_page.get_by_role("heading", name="Login Page", exact=True)).to_be_visible()


def test_02_login_form_elements(login_page):
    expect(login_page.locator("#username")).to_be_visible()
    expect(login_page.locator("#password")).to_have_attribute("type", "password")
    expect(login_page.get_by_role("button", name="Login")).to_be_enabled()


def test_03_login_with_valid_credentials(login_page):
    login(login_page, VALID_USERNAME, VALID_PASSWORD)

    expect(login_page).to_have_url(re.compile(r".*/secure$"))
    expect(login_page.get_by_role("heading", name="Secure Area", exact=True)).to_be_visible()
    expect(login_page.locator("#flash")).to_contain_text("You logged into a secure area!")


def test_04_login_with_invalid_username(login_page):
    login(login_page, "wrong_user", VALID_PASSWORD)

    expect(login_page.locator("#flash")).to_contain_text("Your username is invalid!")


def test_05_login_with_invalid_password(login_page):
    login(login_page, VALID_USERNAME, "wrong_password")

    expect(login_page.locator("#flash")).to_contain_text("Your password is invalid!")


def test_06_submit_empty_fields(login_page):
    login_page.get_by_role("button", name="Login").click()

    expect(login_page.locator("#flash")).to_contain_text("Your username is invalid!")


def test_07_logout_after_login(login_page):
    login(login_page, VALID_USERNAME, VALID_PASSWORD)
    login_page.get_by_role("link", name="Logout").click()

    expect(login_page).to_have_url(LOGIN_URL)
    expect(login_page.locator("#flash")).to_contain_text("You logged out of the secure area!")