from scrapper.freshProduceScrapper import FreshProduceArticlesScrapper
from models.article import Article
from fileutils.csvHandler import CSVHandler
import asyncio
from ai.gemini import Gemini


if __name__ == "__main__":
    scrapper = FreshProduceArticlesScrapper(["Global Trade","Food Safety","Technology"])
    async def main():
        #First stage: Web scrapping and saving it in a CSV file
        scraped_filepath = "scraped_data.csv"
        articles = await scrapper.scrape()
        articles_as_dict = (article.basic_info() for article in articles)
        CSVHandler.write(scraped_filepath, articles_as_dict)

        #Second Stage: AI must get a summary and a topics list for each summary
        analysis_filepath = "analysis_summary.csv"
        geminiAI = Gemini()
        for article in articles:
            summary, topics = geminiAI.summarize_article(article.title,article.full_article_text)
            article.add_analysis(summary,topics)

        articles_as_dict = (article.full_info() for article in articles)
        CSVHandler.write(analysis_filepath,articles_as_dict)
        

        
    #asyncio.run(main())