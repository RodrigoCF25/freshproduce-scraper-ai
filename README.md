
# Web Scraping & Analysis of FreshProduce.com Articles

## Description

This project collects and analyzes articles from FreshProduce.com to identify trends and key insights related to global trade, food safety, and technology in the fresh produce industry. The data is scraped from the website, analyzed using AI for summaries and key topics, and stored in a structured format for easy use.

## Features

- Web scraping of articles from FreshProduce.com in three categories: Global Trade, Food Safety, Technology.
- Use of Pipenv for dependency management.
- AI-based analysis using Gemini API to generate summaries and extract key topics from each article.
- Data is saved in a structured CSV format for easy analysis, including scraped data along with AI-generated summaries and key topics.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/your-repo.git
   ```

2. Navigate to the project directory:
   ```
   cd your-repo
   ```

3. Install dependencies with Pipenv:
   ```
   pipenv install
   ```
   or
   ```
   pipenv install -r requirements.txt
   ```

   This will install all required dependencies listed in `Pipfile`, including:
   - playwright for web scraping
   - python-dotenv for environment variable management
   - google-genai for generating AI summaries and key topics

5. If you need to activate the virtual environment:
   ```
   pipenv shell
   ```

6. Create a .env file
In the root directory, create a .env file and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

If you want to exit the virtual environment:
   ```
   exit
   ```

## Usage

### Scraping and Analyzing Articles

To scrape articles from FreshProduce.com, analyze them with AI (summarizing and extracting key topics), and save the results in a CSV file, simply run the following command while your virtual environment active:

```
python main.py
```

This will execute the following two stages from the `main.py` script:

### 1. Web Scraping

- Scrapes articles from the Global Trade, Food Safety, and Technology categories on FreshProduce.com.
- The scraping is handled by the `FreshProduceArticlesScraper` class in the `scrapper.freshProduceScrapper.py` file.
- The articles are stored with the following information: title, URL, category, and full article text.
- The data is saved in a CSV file called `scraped_data.csv`.

#### Code reference for web scraping:

```python
# Stage 1: Web scraping and saving the data
scraped_filepath = "scraped_data.csv"
articles = await scrapper.scrape()
articles_as_dict = (article.core_info() for article in articles)

# Saving the scraped data
CSVHandler.write(scraped_filepath, articles_as_dict)
```

#### Example of the `scraped_data.csv` file:

| title            | url                  | category       | full_article_text |
|------------------|----------------------|----------------|-------------------|
| Article 1 Title  | article 1 url        | Global Trade   | Full article text... |
| Article 2 Title  | article 2 url        | Food Safety    | Full article text... |
| Article 3 Title  | article 3 url        | Technology     | Full article text... |

### 2. AI Analysis

After scraping, the articles are passed to the Gemini AI for summarization and key topic extraction.
- The data is then merged with the AI-generated insights (summary and key topics).
- The combined data (article title, URL, category, full article text, summary, and key topics) is saved in a new CSV file called `analysis_summary.csv`.

#### Code reference for AI analysis:

```python
# Stage 2: AI Analysis and saving the insights
analysis_filepath = "analysis_summary.csv"
geminiAI = Gemini()

for article in articles:
    summary, topics = geminiAI.summarize_article(article.title, article.full_article_text)
    article.add_insights(summary, topics)

articles_as_dict = (article.with_insights() for article in articles)

# Saving the combined data
CSVHandler.write(analysis_filepath, articles_as_dict)
```

#### Example of the `analysis_summary.csv` file:

| title            | url                  | category       | full_article_text | summary            | topics                                        |
|------------------|----------------------|----------------|-------------------|--------------------|-----------------------------------------------|
| Article 1 Title  | article 1 url        | Global Trade   | Full article text... | Summary of the article... | ["Topic1", "Topic2", "Topic3", "Topic4", "Topic5"] |
| Article 2 Title  | article 2 url        | Food Safety    | Full article text... | Summary of the article... | ["Topic1", "Topic2", "Topic3", "Topic4", "Topic5"]     |
| Article 3 Title  | article 3 url        | Technology     | Full article text... | Summary of the article... | ["Topic1", "Topic2", "Topic3", "Topic4", "Topic5"]                |

## Dependencies

This project uses the following dependencies:
- **Pipenv** for environment and dependency management.
- **playwright** for web scraping.
- **python-dotenv** for managing environment variables.
- **google-genai** for generating AI summaries and extracting key topics.
