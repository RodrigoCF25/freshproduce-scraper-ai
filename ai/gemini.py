import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

class Gemini:
    def __init__(self):
        #Load API KEY
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env")
        self.client = genai.Client(api_key=api_key)

    def summarize_article(self, title: str, text: str) -> tuple[str,list[str]]:
        default_summary = ""
        default_topics = []

        if title.strip() == "" or text.strip() == "":
            print("[INFO]: an article does not have a title or text")
            return (default_summary, default_topics)

        prompt = f"""
    You are a helpful assistant. I will give you the title and full text of an article.

    Return your answer in valid JSON format using the following structure:

    {{
    "summary": "<one-sentence summary of the article>",
    "topics": ["topic1", "topic2", "topic3"] just 3-5 primary topics or keywords from the text
    }}

    Here is the article:

    Title: {title}
    Text: {text}
    """
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=512,
                    system_instruction="You are a helpful assistant that extracts summaries and topics from articles and returns them in JSON format."
                )
            )

            raw_text = response.text.strip()

            
            if raw_text.startswith("```"):
                raw_text = raw_text.strip("```").strip()
                if raw_text.lower().startswith("json"):
                    raw_text = raw_text[4:].strip()

            json_answer = json.loads(raw_text)
            summary = json_answer["summary"]
            topics = json_answer["topics"]
            return (summary,topics)

        except Exception as e:
            print(f"Error analyzing article: {e}")
            return (default_summary,default_topics)

