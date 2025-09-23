from playwright.sync_api import Page
import time

class CareerPathsPage:
    CAREER_NAV_XPATH = (
        "//button[starts-with(normalize-space(), 'Career')] | "
        "//a[starts-with(normalize-space(), 'Career')]"
    )
    CAREER_PATHS_OPTION_XPATH = (
        "//a[contains(normalize-space(),'Career Paths')] | "
        "//button[contains(normalize-space(),'Career Paths')] | "
        "//span[normalize-space()='Career Paths']"
    )
    INSPIRATION_SECTION_XPATH = (
        "//*[contains(translate(normalize-space(text()),'INSPIRATION','inspiration'),'inspiration')]"
    )
    VIEW_CAREER_PATH_BUTTON_ROLE = ("button", "View career path")
    CAREER_PATH_BREADCRUMB_XPATH = (
        "//button[@aria-label='Career Paths' or normalize-space(text())='Career Paths'] | "
        "//span[contains(@class,'BreadcrumbItem-module_child__yJKqC') and normalize-space(text())='Career Paths']"
    )
    CARD_TITLE_SELECTOR = "a.title__NqdfV"

    def __init__(self, page: Page):
        self.page = page

    def go_to_career_paths(self):
        career_nav = self.page.locator(self.CAREER_NAV_XPATH)
        career_nav.wait_for(state="visible", timeout=60000)
        try:
            career_nav.first.hover()
            time.sleep(3)
        except Exception:
            pass
        career_nav.first.click()
        option = self.page.locator(self.CAREER_PATHS_OPTION_XPATH)
        option.wait_for(state="visible", timeout=10000)
        option.click()

    def scroll_to_inspiration(self):
        found = False
        for _ in range(20):  # Try up to 20 times
            section = self.page.locator(f"xpath={self.INSPIRATION_SECTION_XPATH}")
            count = section.count()
            if count > 0:
                for i in range(count):
                    try:
                        text = section.nth(i).inner_text().strip()
                        if 'inspiration' in text.lower():
                            section.nth(i).scroll_into_view_if_needed()
                            found = True
                            break
                    except Exception:
                        pass
                if found:
                    break
            self.page.mouse.wheel(0, 500)  # Scroll down
            time.sleep(0.5)
        if not found:
            print("[WARNING] Could not find any element containing 'inspiration' after scrolling.")
        time.sleep(1)

    def visit_first_n_career_cards(self, n=3):
        card_names = []
        for idx in range(n):
            if idx > 0:
                card_to_scroll = self.page.get_by_role("button", name="View career path").nth(idx)
                card_to_scroll.scroll_into_view_if_needed()
                time.sleep(0.5)
            card_title = self.page.get_by_role("button", name="View career path").nth(idx).evaluate(
                "el => el.closest('.careerCardV2Wrapper__cg_VH').querySelector('a.title__NqdfV')?.innerText || '(no title found)'"
            )
            card_names.append(card_title.strip())
            self.page.get_by_role("button", name="View career path").nth(idx).click(force=True)
            # Wait for and click the breadcrumb to return
            breadcrumb = self.page.locator(self.CAREER_PATH_BREADCRUMB_XPATH)
            breadcrumb.wait_for(state="visible", timeout=10000)
            breadcrumb.first.click()
            time.sleep(1)
        return card_names

    def go_home_and_scroll_recently_viewed(self):
        home_btn = self.page.locator("xpath=//button[contains(@class,'navItemTitle') and @aria-label='Home']")
        home_btn.first.click()
        recently_viewed = self.page.locator("xpath=//*[contains(translate(normalize-space(text()),'RECENTLY','recently'),'recently viewed careers')]")
        recently_viewed.wait_for(state="visible", timeout=10000)
        recently_viewed.scroll_into_view_if_needed()
        time.sleep(3)

    def get_recently_viewed_card_names(self, n=3):
        all_cards = self.page.locator('.careerCardV2Wrapper__cg_VH')
        viewed_names = []
        for i in range(n):
            if all_cards.count() > i:
                card = all_cards.nth(i)
                title_el = card.locator(self.CARD_TITLE_SELECTOR)
                if title_el.count() > 0:
                    name = title_el.first.inner_text().strip()
                else:
                    name = '(not found)'
                viewed_names.append(name)
            else:
                viewed_names.append('(not found)')
        return viewed_names
