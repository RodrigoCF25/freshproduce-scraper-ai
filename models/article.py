from dataclasses import dataclass, asdict
from typing import Any, Optional, List

@dataclass
class Article:
    title: str
    url: str
    category : str
    full_article_text : str
    summary : Optional[str] = None
    topics : Optional[List[str]] = None

    def core_info(self) -> dict[str, Any]:
        """
        Returns the core article information (excluding AI analysis).

        Returns:
            dict[str, Any]: Dictionary containing title, url, category, and full text.
        """
        return{
            "title" : self.title,
            "url" : self.url,
            "category": self.category,
            "full_article_text" : self.full_article_text
        }
    
    def add_insights(self, summary:str, topics: List[str]):
        """
        Adds AI-generated insights to the article.

        Args:
            summary (str): One-sentence summary of the article.
            topics (List[str]): List of key topics or keywords.
        """
        self.summary = summary
        self.topics = topics

    def with_insights(self) -> dict[str, Any]:
        """
        Returns all article information including AI analysis.

        Returns:
            dict[str, Any]: Dictionary representation of the full article (includes summary and topics).
        """
        return asdict(self)


    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Article":
        """
        Creates an Article instance from a dictionary.

        Args:
            data (dict[str, Any]): Dictionary containing article data.

        Returns:
            Article: A new instance of Article with fields populated from the dictionary.
        """
        return cls(**data)


    def __repr__(self):
        return f"""Title: {self.title}
URL: {self.url}
Category: {self.category}
FullText: {self.full_article_text}
"""
