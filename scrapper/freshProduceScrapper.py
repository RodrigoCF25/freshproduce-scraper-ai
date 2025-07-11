from scrapper.webScrapper import WebScapper
from models.article import Article
from browser.browserManager import BrowserManager

import asyncio

# Class for web scrapping the Articles of FreshProduce.com given some categories
class FreshProduceArticlesScraper(WebScapper):
    """
    Scrapes articles data from FreshProduce.com based on given categories.
    """

    def __init__(self, categories: list[str], max_pages: int = 5):
        self.__base_url = "https://www.freshproduce.com"
        self.categories = categories
        self.max_pages = max_pages
        self.browser_manager = BrowserManager(max_pages)

    async def scrape(self) -> list[Article]:
        """
        Starts the scraping process for all specified categories.

        Returns:
            list[Article]: List of extracted Article instances.
        """
        try:
            await self.browser_manager.launch(headless=True, slow_mo=200)

            # Get all hrefs (article links) for each category
            category_href_pairs = await asyncio.gather(*[
                self.__get_hrefs_from_category(category) for category in self.categories
            ])

            # Get each article info from each href (URL)
            tasks = []
            for category, hrefs in category_href_pairs:
                for href in hrefs:
                    tasks.append(self.__scrape_article(category, href))

            results = await asyncio.gather(*tasks, return_exceptions=True)
            successful = list(filter(lambda article: article is not None, results))
            failed = len(results) - len(successful)
            print(f"[INFO] Successfully scraped {len(successful)} articles. Failed: {failed}")
            articles = successful
            return articles


        except Exception as e:
            print(f"[ERROR] Scraping process failed: {e}")

        finally:
            await self.browser_manager.close()

        return []


    def __build_filtered_url(self, category: str, page_number: int = 0) -> str:
        formatted = "-".join(category.lower().strip().split(" "))
        return f"{self.__base_url}/resources/{formatted}/?pageNumber={page_number}&filteredCategories=Article"

    async def __get_hrefs_from_category(self, category: str) -> tuple[str, list[str]]:
        """
            Retrieves all article hrefs for a given category

            Args:
                category (str): The category to scrape links from.

            Returns:
                tuple[str, list[str]]: The category and list of relative href strings.
        """

        page = await self.browser_manager.get_page()
        try:
            page_number = 0
            hrefs = []

            # Go first to check if Article filter exists for that category
            url = self.__build_filtered_url(category, page_number)
            await page.goto(url)
            article_check_button = await page.query_selector("input[name=Article]")
            if not article_check_button:
                print(f"[INFO] No 'Article' checkbox for category: {category}")
                return (category, [])

            # Continue pagination
            while True:
                url = self.__build_filtered_url(category, page_number)
                await page.goto(url)
                await page.wait_for_selector("div.result-panel a", timeout=10_000)

                links = await page.query_selector_all("div.result-panel a")
                href_tasks = [link.get_attribute("href") for link in links]
                current_hrefs = await asyncio.gather(*href_tasks)
                hrefs.extend(filter(None, current_hrefs))

                next_button = await page.query_selector('div.next button.score-button.secondary')
                if not next_button or await next_button.get_attribute("disabled") is not None:
                    break

                page_number += 1

            return (category, hrefs)

        except Exception as e:
            print(f"[ERROR] Category {category}: {e}")
            return (category, [])
        finally:
            await self.browser_manager.release_page(page)

    async def __scrape_article(self, category: str, href: str) -> Article | None:
        """
        Scrapes the title and full text of an article given its href.

        Args:
            category (str): The category the article belongs to.
            href (str): The relative path to the article.

        Returns:
            Article | None: The extracted Article object, or None if extraction failed.
        """
        page = await self.browser_manager.get_page()
        try:
            article_url = f"{self.__base_url}{href}"
            await page.goto(article_url)

            title_task = self.__get_title(page)
            content_task = self.__get_full_article_text(page)
            title, content = await asyncio.gather(title_task, content_task)

            if title and content:
                return Article(title, article_url, category, content)

        except Exception as e:
            print(f"[ERROR] Article {href}: {e}")
        finally:
            await self.browser_manager.release_page(page)

        return None


    async def __get_title(self, page) -> str | None:
        """
        Extracts the title from the article page.

        Args:
            page (Page): The Playwright page object currently loaded with the article.

        Returns:
            str | None: The title text if found, otherwise None.
        """
        
        try:
            h1 = await page.query_selector("h1")
            return await h1.inner_text() if h1 else None
        except Exception as e:
            print(f"[ERROR] Extracting title: {e}")
            return None

    async def __get_full_article_text(self, page) -> str | None:
        """
        Extracts the full body content from the article page.

        Args:
            page (Page): The Playwright page object currently loaded with the article.

        Returns:
            str | None: The largest text block found in the article content, or None.
        """
        try:
            content_divs = await page.query_selector_all('div[data-epi-type="content"]')
            if content_divs:
                texts = [await div.inner_text() for div in content_divs]
                return max(texts, key=lambda t: len(t.strip()), default=None)
        except Exception as e:
            print(f"[ERROR] Extracting article text: {e}")
        return None
