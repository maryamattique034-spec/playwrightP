import re
from playwright.sync_api import Page, expect
from pathlib import Path

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

# Test login with two-factor authentication
def test_get_input(page: Page):
    page.goto("https://the-internet.herokuapp.com/two_factor")

    # Expects page to have a heading with the name of Installation.
    expect(page.get_by_role("heading", name="Two-Factor Login")).to_be_visible()

    expect(page.get_by_text("Log in with")).to_be_visible()

    page.get_by_label("Username").fill("tomsmith")

    page.get_by_label('password').focus()
    
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


# Test hover and click
def test_hover_and_click(page: Page):
    page.goto("https://the-internet.herokuapp.com/hovers")

    # Hover over the first figure
    first_figure = page.locator(".figure").nth(0)
    first_figure.hover()

    # Click on the "View profile" link that appears after hovering
    first_figure.get_by_role("link", name="View profile").click()

    # Expect the new page to have a heading with the name of Not Found.
    expect(page.get_by_role("heading", name="Not Found")).to_be_visible()


# Test file upload
def test_file_upload(page: Page):
    page.goto("https://the-internet.herokuapp.com/upload")

    with page.expect_file_chooser() as fc_info:
        file_id = page.locator('#file-upload').click()
    #    file_id = page.locator('input[name="file"]').click()

    file_chooser = fc_info.value
    file_chooser.set_files("samplepdf.pdf")

    page.get_by_role("button", name="Upload").click()

    expect(page.get_by_text("File Uploaded!")).to_be_visible()


def test_download_file(page: Page):
    # 1. Navigate to the page with the download link/button
    page.goto("https://the-internet.herokuapp.com/download")

    # 2. Use a context manager to wait for the download event while clicking
    with page.expect_download() as download_info:
        # 3. Click the element that initiates the download
        page.get_by_role("link", name="Images.txt").click()
    # 4. Get the download object from the context manager
    download = download_info.value

    # Optional: Inspect the suggested filename
    print(f"Suggested filename: {download.suggested_filename}")

    # 5. Define the local directory and path to save the file
    downloads_dir = Path(__file__).parent / "downloads"
    downloads_dir.mkdir(exist_ok=True)
    save_path = downloads_dir / download.suggested_filename

    # 6. Save the downloaded file to your desired path
    download.save_as(save_path)

    # 7. Verify the file exists locally
    assert save_path.exists()
    print(f"File successfully saved to: {save_path}")


def test_select_dropdown(page: Page):
    # 1. Navigate to the page with the dropdown
    page.goto("https://the-internet.herokuapp.com/dropdown")

    expect(page.get_by_role("heading", name="Dropdown List")).to_be_visible()
    # 2. Select an option by its visible text
    page.locator("#dropdown").select_option("Option 2")

    # Alternatively, you can select by value or index:
    # page.locator("#country-select").select_option(value="ca")
    # page.locator("#country-select").select_option(index=1)

    # 3. Verify the selection was successful
    selected_option = page.locator("#dropdown")
    expect(selected_option).to_have_value("2") # Or verify the visible text



def test_select_drag_drop(page: Page):
    # 1. Navigate to the page with the dropdown
    page.goto("https://the-internet.herokuapp.com/drag_and_drop")

    expect(page.get_by_role("heading", name="Drag and Drop")).to_be_visible()

    source = page.locator("#column-a")
    target = page.locator("#column-b")

    # 3. Perform the drag and drop action
    source.drag_to(target)

    # 4. Verify the action was successful
    # (In this specific example, Column A and Column B swap places)
    expect(page.locator("#column-a header")).to_have_text("B")


def test_dynamic_loading(page: Page):
    # 1. Navigate to the page with the dropdown
    page.goto("https://the-internet.herokuapp.com/dynamic_loading/2")

    expect(page.get_by_role("heading", name="Dynamically Loaded Page Elements")).to_be_visible()

    page.get_by_role("button", name="Start").click()

    expect(page.locator("#finish")).to_have_text("Hello World!", timeout=10000)
    # page.locator("#finish").text_content()



def test_dynamic_controls(page: Page):
    # 1. Navigate to the page with the dropdown
    page.goto("https://the-internet.herokuapp.com/dynamic_controls")

    expect(page.locator("#checkbox")).to_have_count(1)

    page.get_by_role("button", name="Remove").click()

    expect(page.locator("#checkbox")).to_have_count(0)

    expect(page.locator("#message")).to_have_text("It's gone!")

    page.get_by_role("button", name="Add").click()

    expect(page.locator("#message")).to_have_text("It's back!")

    expect(page.get_by_role("textbox")).to_be_disabled()

    page.get_by_role("button", name="Enable").click()

    expect(page.locator("#message")).to_have_text("It's enabled!")

    expect(page.get_by_role("textbox")).to_be_enabled()

    page.get_by_role("textbox").fill("Maryam Attique")

    expect(page.get_by_role("textbox")).to_have_value("Maryam Attique")



def test_entry_ad(page: Page):
    page.goto("https://the-internet.herokuapp.com/entry_ad")

    modal = page.locator("#modal")

    # 1. Modal appears automatically (auto-wait via expect)
    expect(modal).to_be_visible()
    expect(modal.locator(".modal-title")).to_contain_text("This is a modal window")

    # 2. Close it
    modal.locator(".modal-footer").click()
    expect(modal).to_be_hidden()

    # 3. Reload: the cookie stops the ad from showing again
    page.reload()
    page.wait_for_timeout(2000)  # only for learning: gives the ad time to (not) appear
    expect(modal).to_be_hidden()

    # # 4. Re-enable the ad and reload: it shows again
    # page.locator("#restart-ad").click()
    # page.reload()
    # expect(modal).to_be_visible()


def test_exit_intent(page: Page):
    page.goto("https://the-internet.herokuapp.com/exit_intent")

    modal = page.locator("#ouibounce-modal")
    expect(modal).to_be_hidden()  # not shown yet

    # Move the mouse inside the page, then fire the "mouse left the page" event
    page.mouse.move(300, 300)
    page.locator("html").dispatch_event("mouseleave", {"clientY": -1})

    expect(modal).to_be_visible()
    expect(modal.locator(".modal-title")).to_contain_text("This is a modal window")

    modal.locator(".modal-footer").click()
    expect(modal).to_be_hidden()


