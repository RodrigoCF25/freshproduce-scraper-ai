from playwright.async_api import async_playwright, Page, Browser
from asyncio import Semaphore
import asyncio

class BrowserManager:
    
    def __init__(self, max_pages: int = 5):
        self.max_pages = max_pages
        self.page_pool: list[Page] = []
        self.page_semaphore = Semaphore(max_pages)
        self.browser: Browser | None = None
        self.playwright = None

    async def launch(self, headless: bool = True, slow_mo: int = 200):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=headless, slow_mo=slow_mo)
        self.page_pool = [await self.browser.new_page() for _ in range(self.max_pages)]

    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def get_page(self) -> Page:
        async with self.page_semaphore:
            while True:
                for page in self.page_pool:
                    if not hasattr(page, "_in_use") or not page._in_use:
                        page._in_use = True
                        return page
                await asyncio.sleep(0.1)

    async def release_page(self, page: Page):
        page._in_use = False
