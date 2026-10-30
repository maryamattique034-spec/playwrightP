import re
from playwright.sync_api import Page, expect
def test_has_title(page: Page):
    page.goto("https://playwright.dev/")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Playwright"))

def test_get_started_link(page: Page):
    page.goto("https://playwright.dev/")

    # Click the get started link.
    page.get_by_role("link", name="Get started").click()

    # Expects page to have a heading with the name of Installation.
    expect(page.get_by_role("heading", name="Installation")).to_be_visible()

    expect(page.get_by_text("How to install Playwright")).to_be_visible()


def test_get_input(page: Page):
    page.goto("https://the-internet.herokuapp.com/two_factor")

    # Expects page to have a heading with the name of Installation.
    expect(page.get_by_role("heading", name="Two-Factor Login")).to_be_visible()

    expect(page.get_by_text("Log in with")).to_be_visible()

    page.get_by_label("Username").fill("tomsmith")

    page.get_by_label("Password").fill("SuperSecretPassword!")

    page.get_by_role("button", name="Next").click()

    expect(page.get_by_text("Enter Your Code")).to_be_visible()

    








 
    