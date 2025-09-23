from playwright.sync_api import Page

class CommunityPage:
    COMMUNITY_BUTTON_XPATH = (
        "//button[contains(@class,'navItemTitle') and @aria-label='Community']"
    )
    MESSAGE_BUTTONS_XPATH = "//button[normalize-space()='Message']"
    MESSAGE_INPUT_XPATH = (
        "//div[@role='textbox' or @contenteditable='true' or contains(@data-placeholder,'Start writing')]"
    )
    SEND_NOW_BUTTON_XPATH = "//button[contains(text(),'Send Now')]"
    SEND_WITHOUT_MEETING_XPATH = "//button[contains(text(),'Send without meeting')]"
    GO_TO_INBOX_LINK_XPATH = "//button[contains(text(),'Go to inbox')]"
    MESSAGE_BUBBLE_CONTAINS_TEXT_XPATH = (
        "//div[contains(@class,'rich-text') and contains(@class,'ql-editor')]/p[contains(text(),'Hello')]"
    )

    def __init__(self, page: Page):
        self.page = page

    def send_and_verify_message(self, next_index, save_next_index_fn):
        self.page.locator(self.COMMUNITY_BUTTON_XPATH).wait_for(state="visible", timeout=60000)
        self.page.locator(self.COMMUNITY_BUTTON_XPATH).click()
        message_buttons = self.page.locator(self.MESSAGE_BUTTONS_XPATH)
        message_buttons.first.wait_for(state="visible", timeout=60000)
        total = message_buttons.count()
        assert total > 0, "No message buttons found on the Community page."
        index_to_use = next_index % total
        message_buttons.nth(index_to_use).click()
        self.page.locator(self.MESSAGE_INPUT_XPATH).wait_for(state="visible", timeout=30000)
        self.page.locator(self.MESSAGE_INPUT_XPATH).fill("Hello")
        self.page.locator(self.SEND_NOW_BUTTON_XPATH).wait_for(state="visible", timeout=10000)
        self.page.locator(self.SEND_NOW_BUTTON_XPATH).click()
        self.page.locator(self.SEND_WITHOUT_MEETING_XPATH).wait_for(state="visible", timeout=30000)
        self.page.locator(self.SEND_WITHOUT_MEETING_XPATH).click()
        self.page.locator(self.GO_TO_INBOX_LINK_XPATH).wait_for(state="visible", timeout=60000)
        self.page.locator(self.GO_TO_INBOX_LINK_XPATH).click()
        self.page.locator(self.MESSAGE_BUBBLE_CONTAINS_TEXT_XPATH).wait_for(state="visible", timeout=60000)
        assert self.page.locator(self.MESSAGE_BUBBLE_CONTAINS_TEXT_XPATH).is_visible(), (
            "The 'Hello' message did not appear in the inbox conversation."
        )
        save_next_index_fn(index_to_use + 1)
