from scrapper.webScrapper import WebScapper
from playwright.async_api import async_playwright
import asyncio
from models.article import Article
from utils.text import TextFormatter


class FreshProduceArticlesScrapper(WebScapper):

    def __init__(self,categories):
        self.__base_url = "https://www.freshproduce.com"
        self.categories = categories
    
    async def scrape(self) -> list[Article]:
        articles = []
        async with async_playwright() as p:
            try:
                browser = await p.chromium.launch(headless=True, slow_mo=200)
                page = await browser.new_page()
            
                for category in self.categories:
                    try:
                        filtered_url = self.__build_filtered_url(category)
                        await page.goto(filtered_url)
                    
                        await page.wait_for_selector("div.result-panel a")
                        article_links = await page.query_selector_all("div.result-panel a")

                        hrefs_tasks = (link.get_attribute("href") for link in article_links)
                        hrefs = await asyncio.gather(*hrefs_tasks)
                        hrefs = filter(lambda href: href, hrefs)

                        for href in hrefs:
                            try:
                                article_url = f"{self.__base_url}{href}"
                                await page.goto(article_url)
                                title_task = self.getTitle(page)
                                full_article_text_task = self.get_full_article_text(page)
                                title, full_article_text = await asyncio.gather(*[title_task,full_article_text_task])
                                article = Article(title,article_url,category,full_article_text)
                                articles.append(article)
                                await page.go_back()

                            except Exception as e:
                                print(f"[ERROR] Al visitar artículo: {href} — {e}")

                    except Exception as e:
                        print(f"[ERROR] Al procesar categoría '{category}': {e}")

            except Exception as e:
                print(f"[ERROR] Al iniciar navegador o playwright: {e}")

            finally:
                await page.close()
                
        return articles


    async def getTitle(self,page):
        try:
            pass
            h1 = await page.query_selector("h1")
            title = await h1.inner_text()
            cleaned_title = TextFormatter.clean_text(title)
            return cleaned_title
        
        except Exception as e:
            print(f"Error extracting title: {e}")    

        return None
    
    async def get_full_article_text(self, page):
        try:
            content_div = await page.query_selector('div[data-epi-type="content"]')

            if content_div:
                paragraph_elements = await content_div.query_selector_all('p')
                text_tasks = (p.inner_text() for p in paragraph_elements)
                
                raw_paragraphs = await asyncio.gather(*text_tasks)
                full_text = "\n".join(raw_paragraphs)
                cleaned_text = TextFormatter.clean_text(full_text)
                return cleaned_text
            
        
        except Exception as e:
            print(f"Error extracting paragraph text: {e}")
        
        return None


    def __build_filtered_url(self, category: str, page: int = 0) -> str:
        formatted_category = "-".join(category.lower().strip().split(" "))
        return f"{self.__base_url}/resources/{formatted_category}/?pageNumber={page}&filteredCategories=Article"

