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
    CONTACT_NAME_XPATH = (
        ".//span[contains(@class,'contact') or contains(@class,'name') or contains(@class,'user') or contains(@class,'person') or contains(@class,'profile')] | "
        ".//a[contains(@class,'contact') or contains(@class,'name') or contains(@class,'user') or contains(@class,'person') or contains(@class,'profile')]"
    )

    def __init__(self, page: Page):
        self.page = page

    def extract_and_print_all_jobs(self, job_xpaths, max_contacts=3):
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
        for job_card_xpath, job_title_xpath, job_label in job_xpaths:
            job_card = self.page.locator(job_card_xpath).first
            job_card.wait_for(state="visible", timeout=60000)
            job_title = job_card.locator(f"xpath={job_title_xpath}").first.inner_text().strip()
            contact_els = job_card.locator(f"xpath={self.CONTACT_NAME_XPATH}")
            contacts = []
            for i in range(max_contacts):
                if contact_els.nth(i).count() > 0:
                    try:
                        contact_text = contact_els.nth(i).inner_text().strip()
                        if contact_text:
                            contacts.append(contact_text)
                    except Exception:
                        break
            print(f"\n[RESULT] {job_label}")
            print(f"  Job title: {job_title}")
            for idx, contact in enumerate(contacts, 1):
                print(f"  Recommended contact {idx}: {contact}")
            if not contacts:
                print("  No recommended contacts found.")
