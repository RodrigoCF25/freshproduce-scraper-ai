from scrapper.freshProduceScrapper import FreshProduceArticlesScrapper
from models.article import Article
from fileutils.csvHandler import CSVHandler
import asyncio
from dataclasses import asdict

if __name__ == "__main__":
    scrapper = FreshProduceArticlesScrapper(["Global Trade","Food Safety","Technology"])
    async def main():
        articles = await scrapper.scrape()
        CSVHandler.write("./data.csv", [asdict(article) for article in articles])
        for n,article in enumerate(articles,1):
            print(n)
            print(article)

        print("-------------"*10,"\n")
        articles_read = CSVHandler.read_as("./data.csv",Article.from_dict)

        for n,article in enumerate(articles,1):
            print(n)
            print(article)
        
    asyncio.run(main())