from scrapper.freshProduceScrapper import FreshProduceArticlesScrapper
from fileutils.csvHandler import CSVHandler
import asyncio
from dataclasses import asdict

if __name__ == "__main__":
    scrapper = FreshProduceArticlesScrapper(["Global Trade","Food Safety","Technology"])
    async def main():
        articles = await scrapper.scrape()
 
        for n,article in enumerate(articles,1):
            print(n)
            print(article)

        
    asyncio.run(main())