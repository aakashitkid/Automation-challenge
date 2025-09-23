import json
import os
import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.community_page import CommunityPage
from pages.jobs_page import JobsPage

USER_EMAIL = "aakash@expf.com"
USER_PASSWORD = "Automation@123"
LOGIN_URL = "https://basecopy5.staging.pg-test.com/hub/newhub503949860203/auth/sign-in"

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

        # Login
        login_page = LoginPage(page, LOGIN_URL, USER_EMAIL, USER_PASSWORD)
        login_page.login()

        # Community
        community_page = CommunityPage(page)
        community_page.goto_community()
        index_to_use, total = community_page.send_message(next_index)
        community_page.verify_message_in_inbox()
        save_next_index(index_to_use + 1)

        # Jobs
        jobs_page = JobsPage(page)
        jobs_page.goto_jobs()
        job_title, contacts = jobs_page.extract_job_contacts(SOFTWARE_JOB_CARD_XPATH, SOFTWARE_JOB_TITLE_XPATH, max_contacts=3)
        print(f"\n[RESULT] Software Developer card")
        print(f"  Job title: {job_title}")
        for idx, contact in enumerate(contacts, 1):
            print(f"  Recommended contact {idx}: {contact}")
        if not contacts:
            print("  No recommended contacts found.")
        eng_job_title, eng_contacts = jobs_page.extract_job_contacts(SOFTWARE_ENG_CARD_XPATH, SOFTWARE_ENG_TITLE_XPATH, max_contacts=3)
        print(f"\n[RESULT] Software Engineer card")
        print(f"  Job title: {eng_job_title}")
        for idx, contact in enumerate(eng_contacts, 1):
            print(f"  Recommended contact {idx}: {contact}")
        if not eng_contacts:
            print("  No recommended contacts found.")
        context.close()
        browser.close()
