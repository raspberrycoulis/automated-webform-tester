import json
import time
import random
import requests
import os
from playwright.sync_api import sync_playwright
from playwright_recaptcha import recaptchav3
from urllib.parse import urlparse, parse_qs, unquote
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

form_url = os.getenv("WEBFORM_URL")
webhook_url = os.getenv("WEBHOOK_URL")

def send_teams_alert(status, error_msg):
    payload = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.4",
                    "body": [
                        {
                            "columns": [
                                {
                                    "width": "auto",
                                    "items": [
                                        {
                                            "type": "Icon",
                                            "name": "Form",
                                            "color": "Attention",
                                        }
                                    ],
                                    "type": "Column",
                                },
                                {
                                    "width": "stretch",
                                    "items": [
                                        {
                                            "size": "Large",
                                            "text": "Drupal Webform Automated Tester",
                                            "weight": "Bolder",
                                            "wrap": True,
                                            "type": "TextBlock",
                                        }
                                    ],
                                    "verticalContentAlignment": "Center",
                                    "spacing": "Small",
                                    "type": "Column",
                                },
                            ],
                            "spacing": "Small",
                            "type": "ColumnSet",
                        },
                        {
                            "type": "Table",
                            "targetWidth": "AtLeast:Narrow",
                            "columns": [{"width": 1}, {"width": 2}],
                            "rows": [
                                {
                                    "type": "TableRow",
                                    "cells": [
                                        {
                                            "type": "TableCell",
                                            "verticalContentAlignment": "Center",
                                            "items": [
                                                {
                                                    "type": "TextBlock",
                                                    "text": "Form URL",
                                                    "wrap": True,
                                                    "weight": "Bolder",
                                                }
                                            ],
                                        },
                                        {
                                            "type": "TableCell",
                                            "verticalContentAlignment": "Center",
                                            "items": [
                                                {
                                                    "type": "TextBlock",
                                                    "text": f"[{form_url}]({form_url})",
                                                    "wrap": True,
                                                }
                                            ],
                                        },
                                    ],
                                    "verticalCellContentAlignment": "Center",
                                    "spacing": "None",
                                    "horizontalAlignment": "Left",
                                },
                                {
                                    "type": "TableRow",
                                    "cells": [
                                        {
                                            "type": "TableCell",
                                            "items": [
                                                {
                                                    "type": "TextBlock",
                                                    "text": "Status",
                                                    "wrap": True,
                                                    "weight": "Bolder",
                                                }
                                            ],
                                        },
                                        {
                                            "type": "TableCell",
                                            "items": [
                                                {
                                                    "type": "TextBlock",
                                                    "text": f"{status}",
                                                    "wrap": True,
                                                }
                                            ],
                                        },
                                    ],
                                },
                                {
                                    "type": "TableRow",
                                    "cells": [
                                        {
                                            "type": "TableCell",
                                            "items": [
                                                {
                                                    "type": "TextBlock",
                                                    "text": "Details",
                                                    "wrap": True,
                                                    "weight": "Bolder",
                                                }
                                            ],
                                        },
                                        {
                                            "type": "TableCell",
                                            "items": [
                                                {
                                                    "type": "TextBlock",
                                                    "text": f"{error_msg}",
                                                    "wrap": True,
                                                }
                                            ],
                                        },
                                    ],
                                },
                            ],
                            "firstRowAsHeaders": False,
                            "showGridLines": False,
                        },
                        {
                            "type": "Container",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "wrap": True,
                                    "text": "This message has been sent by an automated webform tester, which attempts to submit a specific webform. If you are reading this, please check the webform works by completing it yourself, and if you are still unable to please alert a developer as soon as possible.",
                                    "fontType": "Default",
                                    "color": "Attention",
                                }
                            ],
                            "roundedCorners": False,
                            "showBorder": False,
                            "style": "attention",
                        },
                        {
                            "actions": [
                                {
                                    "title": "View form",
                                    "type": "Action.OpenUrl",
                                    "url": f"{form_url}",
                                    "tooltip": "Open the URL where the form is located in your browser",
                                    "style": "positive",
                                    "iconUrl": "icon:Open",
                                }
                            ],
                            "type": "ActionSet",
                            "targetWidth": "AtLeast:Narrow",
                            "horizontalAlignment": "Left",
                        },
                    ],
                },
            }
        ],
    }
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code != 200:
            print(f"Failed to send Teams alert: {response.status_code} {response.text}")
    except Exception as e:
        print(f"Exception while sending Teams alert: {e}")


def type_slowly(input_box, text):
    # Debugging
    print("Starting to type slowly...")
    input_box.click()
    for char in text:
        input_box.type(char)
        time.sleep(random.uniform(0.07, 0.3))  ## Usually 0.07, 0.3. Higher numbers = slower.


def move_mouse_randomly(page, times=5):
    # Debugging
    print("Moving mouse randomly...")
    for _ in range(times):
        x = random.randint(100, 800)
        y = random.randint(100, 600)
        page.mouse.move(x, y, steps=random.randint(5, 15))
        time.sleep(random.uniform(0.2, 0.6))


def run_test():
    # Debugging
    print("Running Playwright...")
    with sync_playwright() as p:
        CHROMIUM_ARGS = ['--disable-blink-features=AutomationControlled',]
        #browser = p.chromium.launch(headless=False,args=["--disable-blink-features=AutomationControlled"])
        browser = p.chromium.launch(headless=False, args=CHROMIUM_ARGS,ignore_default_args=["--enable-automation"])
        context = browser.new_context(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36")
        page = context.new_page()
        site_key = os.getenv("RECAPTCHA_SITE_KEY")

        page.goto(form_url)

        # Move the mouse around to look more human...
        move_mouse_randomly(page, 4)
        page.mouse.wheel(23, 87)
        time.sleep(1.3)

        # Accept cookies
        try:
            # Debugging
            print("Accepting cookies...")
            page.get_by_role("button", name="Allow all").click()
        except:
            pass

        type_slowly(page.get_by_label("First Name*"), "Fluid")
        type_slowly(page.get_by_label("Second Name*"), "Ideas")
        type_slowly(page.get_by_label("Email*"), "systems@fluid-ideas.co.uk")
        type_slowly(page.get_by_label("Job title*"), "Fluid Webform Automatron")
        type_slowly(page.get_by_label("Company name*"), "Fluid Ideas")
        type_slowly(page.get_by_label("How can the MTC help?*"), "We're making sure the form works.")

        # Move the mouse around to look more human...
        move_mouse_randomly(page, 6)
        page.mouse.wheel(45, 214)

        time.sleep(2)

        # Manually solve reCAPTCHA v3
        # Debugging
        print("Solving reCAPTCHA v3...")
        token = page.evaluate(
            f"""
            () => new Promise((resolve) => {{
                grecaptcha.ready(() => {{
                    grecaptcha.execute("{site_key}", {{ action: "submit" }}).then((token) => {{
                        const textarea = document.querySelector('textarea[name="g-recaptcha-response"]');
                        if (textarea) textarea.value = token;
                        resolve(token);
                    }});
                }});
            }})
        """
        )
        print(f"Generated reCAPTCHA token: {token}")

        # Submit form
        # Debugging
        print("Starting to submit form...")
        # Waits for the page to load first, then clicks the button.
        #with page.expect_navigation(wait_until="load"):
        #    page.get_by_role("button", name="Send enquiry").click()
        
        # Ditch the wait on load and see if this works.
        page.get_by_role("button", name="Send enquiry").click()

        # Get and process final URL
        final_url = page.url
        print(f"Final URL: {final_url}")

        if "%22error%22" in final_url:
            status = "Submission failed!"
            error_msg = "reCAPTCHA validation failed."
            print("Form submission failed!")
            #send_teams_alert(status, error_msg) # Uncomment to send alert on failure
            print("Teams notification sent!")

        if "%22sid%22" in final_url:
            print("Form submitted successfully")
        else:
            status = "Submission failed!"
            error_msg = "Unexpected URL structure. Submission may not have completed correctly."
            print("Form submission failed!")

        browser.close()


if __name__ == "__main__":
    run_test()
