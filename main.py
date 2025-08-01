from scraper.freshProduceScrapper import FreshProduceArticlesScraper
from fileutils.csvHandler import CSVHandler
import asyncio
from ai.gemini import Gemini

#Remember to have a .env file with the env variable GEMINI_API_KEY="{your api key}"

if __name__ == "__main__":
    scrapper = FreshProduceArticlesScraper(["Global Trade","Food Safety","Technology"])
    async def main():
        #First stage: Web scrapping and saving it in a CSV file
        scraped_filepath = "scraped_data.csv"
        articles = await scrapper.scrape()
        articles_as_dict = (article.core_info() for article in articles)
        CSVHandler.write(scraped_filepath, articles_as_dict)
        
        #Second Stage: AI must get a summary and a topics list for each summary. Save articles with these insights in a CSV
        
        analysis_filepath = "analysis_summary.csv"
        geminiAI = Gemini()
        for article in articles:
            summary, topics = geminiAI.summarize_article(article.title,article.full_article_text)
            article.add_insights(summary,topics)

        articles_as_dict = (article.with_insights() for article in articles)
        CSVHandler.write(analysis_filepath,articles_as_dict)

        
    asyncio.run(main())