from scrapper.webScrapper import WebScapper
from playwright.async_api import async_playwright, Page
from models.article import Article
import asyncio
from asyncio import Semaphore

#Class for web scrapping the Articles of FreshProduce.com given some categories
class FreshProduceArticlesScrapper(WebScapper):
    def __init__(self, categories: list[str], max_pages: int = 5):
        self.__base_url = "https://www.freshproduce.com"
        self.categories = categories
        self.max_pages = max_pages
        self.page_pool: list[Page] = []
        self.page_semaphore = Semaphore(max_pages)

    async def scrape(self) -> list[Article]:
        self.articles = []
        async with async_playwright() as p:
            self.browser = await p.chromium.launch(headless=True, slow_mo=200)
            
            #Create pool of pages
            self.page_pool = [await self.browser.new_page() for _ in range(self.max_pages)]

            #Get all hrefs(article links) for each category
            category_href_pairs = await asyncio.gather(*[
                self.__get_hrefs_from_category(category) for category in self.categories
            ])

            #Get each article info of each href(url)
            tasks = []
            for category, hrefs in category_href_pairs:
                for href in hrefs:
                    tasks.append(self.__scrape_article(category, href))

            #Wait for articles been added to list
            await asyncio.gather(*tasks)

            await self.browser.close()
            return self.articles

    #Deliver a page if available (page not being used)
    async def __get_page_from_pool(self) -> Page:
        async with self.page_semaphore:
            while True:
                for page in self.page_pool:
                    if not hasattr(page, "_in_use") or not page._in_use:
                        page._in_use = True
                        return page
                await asyncio.sleep(0.1)

    #Release page ownership
    async def __release_page_to_pool(self, page: Page):
        page._in_use = False

    def __build_filtered_url(self, category: str, page: int = 0) -> str:
        formatted = "-".join(category.lower().strip().split(" "))
        return f"{self.__base_url}/resources/{formatted}/?pageNumber={page}&filteredCategories=Article"

    
    async def __get_hrefs_from_category(self, category: str) -> tuple[str, list[str]]:
        page = await self.__get_page_from_pool()
        try:
            page_number = 0
            hrefs = []

            # Go first to check if Article filter exists for that category
            url = self.__build_filtered_url(category, page_number)
            await page.goto(url)

            
            article_check_button = await page.query_selector("input[name=Article]")
            if not article_check_button:
                print(f"[INFO] There is no 'Article' checkbox for the category: {category}")
                return (category, [])

            #Continue getting urls for articles if there is a next button and is not disabled
            while True:
                url = self.__build_filtered_url(category, page_number)
                await page.goto(url)
                await page.wait_for_selector("div.result-panel a", timeout=10_000)

                #Get all hrefs (links) for the articles and add them to list
                links = await page.query_selector_all("div.result-panel a")
                href_tasks = [link.get_attribute("href") for link in links]
                current_hrefs = await asyncio.gather(*href_tasks)
                hrefs.extend(filter(None, current_hrefs))

                next_button = await page.query_selector('div.next button.score-button.secondary')
                if not next_button:
                    break
                is_disabled = await next_button.get_attribute("disabled")
                if is_disabled is not None:
                    break

                page_number += 1

            return (category, hrefs)

        except Exception as e:
            print(f"[ERROR] Categoría {category}: {e}")
            return (category, [])
        finally:
            await self.__release_page_to_pool(page)


    #Get the data of an article
    async def __scrape_article(self, category: str, href: str):
        page = await self.__get_page_from_pool()
        try:
            article_url = f"{self.__base_url}{href}"
            await page.goto(article_url)

            # Get title and text
            title_task = self.__get_title(page)
            content_task = self.__get_full_article_text(page)
            title, content = await asyncio.gather(title_task, content_task)

            if title and content:
                article = Article(title, article_url, category, content)
                self.articles.append(article)

        except Exception as e:
            print(f"[ERROR] Artículo {href}: {e}")
        finally:
            await self.__release_page_to_pool(page)

    async def __get_title(self, page: Page) -> str | None:
        try:
            h1 = await page.query_selector("h1")
            if h1:
                title = await h1.inner_text()
                return title
        except Exception as e:
            print(f"[ERROR] Extrayendo título: {e}")
        return None

    async def __get_full_article_text(self, page: Page) -> str | None:
        try:
            content_div = await page.query_selector('div[data-epi-type="content"]')
            if content_div:
                text = await content_div.inner_text()
                return text
            
        except Exception as e:
            print(f"[ERROR] Extrayendo texto del artículo: {e}")
        return None
