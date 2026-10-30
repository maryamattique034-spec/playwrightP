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

    # now input the correct code and verify the login is successful

    # first we have to find the code from the current page fron text 

    # Catch the subheader text containing the message
    # Looking at your HTML, it's inside an h4 with class 'subheader'
    subheader_element = page.locator("h4.subheader")

    message_text = subheader_element.inner_text()

    print(f"Captured text: {message_text}")
    
    # 2. Use a regex pattern to find the 6-digit code
    # \b\d{6}\b searches for 6 consecutive digits bounded by word limits
    match = re.search(r"\b\d{6}\b", message_text)

    if match:
        page.get_by_label("One-time code").fill(match.group(0))
        
        page.get_by_role("button", name="Verify").click()

        expect(page.get_by_text("Secure Area")).to_be_visible()
         
        expect(page.get_by_text("Welcome! You logged in with a password and a one-time code.")).to_be_visible()

        print("Login successful with the 6-digit code.")

    else:
        print("No 6-digit code found in the message.")
        









 
    