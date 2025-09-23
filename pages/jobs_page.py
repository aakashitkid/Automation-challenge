import time
from playwright.sync_api import Page

class JobsPage:
    CAREER_NAV_XPATH = (
        "//button[starts-with(normalize-space(), 'Career')] | "
        "//a[starts-with(normalize-space(), 'Career')]"
    )
    JOBS_OPTION_XPATH = (
        "//a[contains(normalize-space(),'Jobs')] | "
        "//button[contains(normalize-space(),'Jobs')] | "
        "//span[normalize-space()='Jobs']"
    )
    JOBS_PAGE_HEADING_XPATH = (
        "//h1[contains(translate(text(),'JOB','job'),'job')] | "
        "//h2[contains(translate(text(),'JOB','job'),'job')] | "
        "//h3[contains(translate(text(),'JOB','job'),'job')]"
    )
    # Restore the original, more targeted contact extraction logic
    CONTACT_NAME_XPATH = (
        ".//span[contains(@class,'contact') or contains(@class,'name') or contains(@class,'user') or contains(@class,'person') or contains(@class,'profile')] | "
        ".//a[contains(@class,'contact') or contains(@class,'name') or contains(@class,'user') or contains(@class,'person') or contains(@class,'profile')]"
    )

    def __init__(self, page: Page):
        self.page = page

    def extract_and_print_all_jobs(self, max_contacts_list):
        career_nav = self.page.locator(self.CAREER_NAV_XPATH)
        career_nav.wait_for(state="visible", timeout=60000)
        try:
            career_nav.first.hover()
        except Exception:
            pass
        career_nav.first.click()
        self.page.locator(self.JOBS_OPTION_XPATH).wait_for(state="visible", timeout=10000)
        self.page.locator(self.JOBS_OPTION_XPATH).click()
        self.page.locator(self.JOBS_PAGE_HEADING_XPATH).first.wait_for(state="visible", timeout=30000)
        assert self.page.locator(self.JOBS_PAGE_HEADING_XPATH).first.is_visible(), "Jobs page heading not visible"
        time.sleep(1)  # Wait for job cards to fully render

        # Find all job cards
        job_cards = self.page.locator("xpath=//div[contains(@class,'job-card-item')]")
        count = job_cards.count()
        for idx in range(count):
            if idx >= len(max_contacts_list):
                break
            job_card = job_cards.nth(idx)
            try:
                # Try to extract job title
                job_title_el = job_card.locator("xpath=.//div[contains(@class,'job-role')]")
                job_title = job_title_el.first.inner_text().strip()
            except Exception as e:
                print(f"[WARNING] Could not extract job title for card {idx+1}: {e}")
                job_title = "(not found)"
            contacts = []
            seen = set()
            carousel_root = job_card.locator("xpath=.//div[contains(@class, 'job-connections-carousel')]").first
            next_arrow = carousel_root.locator("xpath=.//button[contains(@class, 'Carousel-module_next__') or contains(@aria-label, 'Next connection')]")
            max_contacts = max_contacts_list[idx]
            for _ in range(max_contacts):
                active_slide = carousel_root.locator("xpath=.//div[contains(@class, 'Carousel-module_item__sg5wX') and contains(@id, '-active-slide')]")
                contact_els = active_slide.locator("xpath=.//a[contains(@class, 'username') and contains(@class, 'custom-btn-link')]/span")
                for i in range(contact_els.count()):
                    try:
                        contact_text = contact_els.nth(i).inner_text().strip()
                        if contact_text and contact_text not in seen:
                            contacts.append(contact_text)
                            seen.add(contact_text)
                            if len(contacts) >= max_contacts:
                                break
                    except Exception:
                        continue
                if len(contacts) >= max_contacts:
                    break
                try:
                    if next_arrow.is_enabled():
                        next_arrow.click()
                        time.sleep(1)
                except Exception:
                    break
            print(f"\n[RESULT] Job card {idx+1}")
            print(f"  Job title: {job_title}")
            for cidx, contact in enumerate(contacts, 1):
                print(f"  Contact {cidx}: {contact}")
            if not contacts:
                print("  No contacts found.")
