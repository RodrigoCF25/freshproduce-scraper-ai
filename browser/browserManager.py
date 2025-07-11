from playwright.async_api import async_playwright, Page, Browser
from asyncio import Semaphore
import asyncio

class BrowserManager:
    """
    Manages a pool of browser pages (tabs) using Playwright and an asyncio semaphore
    to limit concurrent access to available pages.
    """
    
    def __init__(self, max_pages: int = 5):
        """
        Initializes the browser manager with a maximum number of pages (tabs).

        Args:
            max_pages (int): The maximum number of browser pages (tabs) to be managed.
        """
        self.max_pages = max_pages
        self.page_pool: list[Page] = []
        self.page_semaphore = Semaphore(max_pages)
        self.browser: Browser | None = None
        self.playwright = None

    async def launch(self, headless: bool = True, slow_mo: int = 200):
        """
        Launches the browser and pre-creates the page pool with 'max_pages' tabs.
        
        Args:
            headless (bool): Whether the browser should run in headless mode (default: True).
            slow_mo (int): The time (in ms) to slow down the actions for debugging purposes (default: 200).
        
        """
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=headless, slow_mo=slow_mo)
        self.page_pool = [await self.browser.new_page() for _ in range(self.max_pages)]

    async def close(self):
        """
        Closes the browser and stops the Playwright instance.
        """
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def get_page(self) -> Page:
        """
        Acquires a free page from the pool. If none are available, waits until one is released.
        
        Returns:
            Page: A Playwright Page object from the pool.
        """
        async with self.page_semaphore:  # Limit access to code inside, only allows up to max_pages concurrent users
            while True:
                for page in self.page_pool:
                    if not hasattr(page, "_in_use") or not page._in_use:
                        page._in_use = True
                        return page
                await asyncio.sleep(0.1)

    async def release_page(self, page: Page):
        """
        Releases a previously acquired page back to the pool.
        
        Args:
            page (Page): The Playwright Page object to be released back to the pool.

        """
        page._in_use = False
