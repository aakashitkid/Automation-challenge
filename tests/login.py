"""
pytest automation script that logs into PeopleGrove staging and rotates
through community users by message-button index.  Each test run clicks the
next available "Message" button and sends a "Hello" message to that user.
An index counter is persisted to ``next_index.json`` in the same
directory as this script to ensure a different user is selected on
subsequent runs.  When the index exceeds the number of message buttons
found on the page, it wraps back to zero.

After verifying the message and navigating to Career > Jobs, the script
locates the Software Developer job card, extracts the job title, grabs the
first recommended contact, clicks the arrow to get the next contact, and
prints a summary of these values at the end.

The browser runs in non-headless mode so you can observe the actions.
"""


import json
import os
import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.community_page import CommunityPage
from pages.jobs_page import JobsPage

# Credentials and login URL
USER_EMAIL = "aakash@expf.com"
USER_PASSWORD = "Automation@123"
LOGIN_URL = "https://basecopy5.staging.pg-test.com/hub/newhub503949860203/auth/sign-in"

# Persistence file for rotating through message buttons
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_FILE = os.path.join(SCRIPT_DIR, "../next_index.json")

SOFTWARE_JOB_CARD_XPATH = (
    "//div[contains(@class,'job') and .//text()[normalize-space()='Software Developer']]"
)
SOFTWARE_JOB_TITLE_XPATH = (
    ".//*[self::h1 or self::h2 or self::h3 or self::div][normalize-space()='Software Developer']"
)
SOFTWARE_ENG_CARD_XPATH = (
    "//div[contains(@class,'job') and .//text()[normalize-space()='Software Engineer']]"
)
SOFTWARE_ENG_TITLE_XPATH = (
    ".//*[self::h1 or self::h2 or self::h3 or self::div][normalize-space()='Software Engineer']"
)


def load_next_index() -> int:
    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            return int(json.load(f))
    except Exception:
        return 0

def save_next_index(index: int) -> None:
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f)

def test_rotate_by_index_nonheadless():
    next_index = load_next_index()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Login (one line)
        LoginPage(page, LOGIN_URL, USER_EMAIL, USER_PASSWORD).do_login()

        # Community (one line)
        CommunityPage(page).send_and_verify_message(next_index, save_next_index)

        # Jobs (one line)
        job_xpaths = [
            (SOFTWARE_JOB_CARD_XPATH, SOFTWARE_JOB_TITLE_XPATH, "Software Developer card"),
            (SOFTWARE_ENG_CARD_XPATH, SOFTWARE_ENG_TITLE_XPATH, "Software Engineer card"),
        ]
        JobsPage(page).extract_and_print_all_jobs(job_xpaths, max_contacts=3)
        context.close()
        browser.close()
