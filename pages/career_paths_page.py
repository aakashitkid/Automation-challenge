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
        # Avoid strict mode violations by operating on the first matched element
        career_nav.first.wait_for(state="visible", timeout=60000)
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
        visited_set = set()

        for _ in range(n):
            # find all career card wrappers and pick the first whose title we haven't visited
            cards = self.page.locator('.careerCardV2Wrapper__cg_VH')
            found_card = None
            for i in range(cards.count()):
                card = cards.nth(i)
                try:
                    title_el = card.locator(self.CARD_TITLE_SELECTOR)
                    if title_el.count() == 0:
                        continue
                    title = title_el.first.inner_text().strip()
                except Exception:
                    continue
                if title not in visited_set:
                    found_card = card
                    card_name = title
                    break

            if not found_card:
                # no more unique cards found
                break

            # scroll the card into view and click its internal 'View career path' button
            try:
                found_card.scroll_into_view_if_needed()
            except Exception:
                pass
            time.sleep(0.3)

            # click the 'View career path' button inside the card
            try:
                view_btn = found_card.get_by_role('button', name='View career path')
                view_btn.click(force=True)
            except Exception:
                # fallback: click any button inside the card
                try:
                    found_card.locator("button").first.click(force=True)
                except Exception:
                    pass

            # wait for navigation and breadcrumb, then return
            try:
                breadcrumb = self.page.locator(self.CAREER_PATH_BREADCRUMB_XPATH)
                breadcrumb.wait_for(state='visible', timeout=15000)
                # stabilize a bit to allow server-side 'recently viewed' update
                time.sleep(1.2)
                breadcrumb.first.click()
            except Exception:
                # attempt a safe navigation back to home
                try:
                    self.page.go_back()
                except Exception:
                    pass

            # small pause to allow UI to refresh
            time.sleep(1.0)

            card_names.append(card_name)
            visited_set.add(card_name)

        return card_names

    def go_home_and_scroll_recently_viewed(self):
        home_btn = self.page.locator("xpath=//button[contains(@class,'navItemTitle') and @aria-label='Home']")
        home_btn.first.click()
        # Robustly find the "Recently viewed" section by scrolling the page in viewport-sized steps
        RECENTLY_XPATH = "//*[contains(translate(normalize-space(text()),'RECENTLY','recently'),'recently')]"
        found = False
        # give the page a bit of time to render after clicking Home
        try:
            self.page.wait_for_load_state("networkidle", timeout=10000)
        except Exception:
            pass

        for attempt in range(40):
            rv = self.page.locator(f"xpath={RECENTLY_XPATH}")
            try:
                count = rv.count()
            except Exception:
                count = 0

            if count > 0:
                for i in range(count):
                    try:
                        text = rv.nth(i).inner_text().strip()
                        if 'recently' in text.lower():
                            rv.nth(i).scroll_into_view_if_needed()
                            # small stabilization pause
                            time.sleep(0.8)
                            found = True
                            break
                    except Exception:
                        pass
                if found:
                    break

            # scroll by one viewport height (more reliable than small wheel deltas)
            try:
                self.page.evaluate("window.scrollBy(0, window.innerHeight)")
            except Exception:
                try:
                    self.page.mouse.wheel(0, 800)
                except Exception:
                    pass
            time.sleep(0.5)

        if not found:
            # Fallback 1: try clicking Home again and give more time
            try:
                home_btn.first.click()
                time.sleep(1)
                self.page.evaluate("window.scrollTo(0, 0)")
                for _ in range(20):
                    rv = self.page.locator(f"xpath={RECENTLY_XPATH}")
                    if rv.count() > 0:
                        rv.first.scroll_into_view_if_needed()
                        found = True
                        break
                    self.page.evaluate("window.scrollBy(0, window.innerHeight)")
                    time.sleep(0.5)
            except Exception:
                pass

        if not found:
            # Final fallback: try the stricter locator with a longer wait
            try:
                fallback = self.page.locator("xpath=//*[contains(translate(normalize-space(text()),'RECENTLY','recently'),'recently viewed careers')]")
                fallback.wait_for(state="visible", timeout=30000)
                fallback.scroll_into_view_if_needed()
                found = True
            except Exception:
                print("[WARNING] Could not find the 'Recently viewed' section after multiple scroll attempts.")

        time.sleep(1)

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
