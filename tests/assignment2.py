import os
import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.career_paths_page import CareerPathsPage

USER_EMAIL = "ashishkk@gmail.com"
USER_PASSWORD = "Automation@123"
LOGIN_URL = "https://basecopy5.staging.pg-test.com/hub/newhub503949860203/auth/sign-in"

def test_career_paths_flow():
	headless_env = os.getenv("HEADLESS", "0")
	headless = headless_env not in ("0", "false", "False", "FALSE")
	with sync_playwright() as p:
		browser = p.chromium.launch(headless=headless)
		context = browser.new_context()
		page = context.new_page()

		# Login
		LoginPage(page, LOGIN_URL, USER_EMAIL, USER_PASSWORD).do_login()

		# Go to Career Paths
		career_paths = CareerPathsPage(page)
		career_paths.go_to_career_paths()
		career_paths.scroll_to_inspiration()

		# Visit first 3 career cards, save names
		card_names = career_paths.visit_first_n_career_cards(3)
		print(f"[RESULT] Card names visited: {card_names}")

		# Go Home and scroll to Recently Viewed
		career_paths.go_home_and_scroll_recently_viewed()

		# Extract recently viewed card names
		viewed_names = career_paths.get_recently_viewed_card_names(3)
		print(f"[RESULT] Recently viewed card names: {viewed_names}")

		# Compare with previously saved card names in reverse order
		reversed_card_names = list(reversed(card_names))
		print(f"[DEBUG] Reversed selected card names: {reversed_card_names}")
		matches = [a == b for a, b in zip(reversed_card_names, viewed_names)]
		print(f"[RESULT] Name matches (reversed): {matches}")
		if all(matches):
			print("[SUCCESS] All recently viewed cards match the selected cards in reverse order.")
		else:
			print("[FAIL] Recently viewed cards do not match the selected cards in reverse order.")

		context.close()
		browser.close()