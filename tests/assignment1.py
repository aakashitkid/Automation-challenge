import json
import os
import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.community_page import CommunityPage
from pages.jobs_page import JobsPage

# Credentials and login URL
USER_EMAIL = "aakash1@gmail.com"
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
	headless_env = os.getenv("HEADLESS", "0")
	headless = headless_env not in ("0", "false", "False", "FALSE")
	with sync_playwright() as p:
		browser = p.chromium.launch(headless=headless)
		context = browser.new_context()
		page = context.new_page()

		# Login (one line)
		LoginPage(page, LOGIN_URL, USER_EMAIL, USER_PASSWORD).do_login()

		# Community (one line)
		CommunityPage(page).send_and_verify_message(next_index, save_next_index)

		# Jobs (one line)
		# Specify how many contacts to extract for each job card (by order on the page)
		max_contacts_list = [4, 2]
		JobsPage(page).extract_and_print_all_jobs(max_contacts_list)
		context.close()
		browser.close()