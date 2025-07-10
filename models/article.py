from dataclasses import dataclass
from typing import Any, Optional, List

@dataclass
class Article:
    title: str
    url: str
    category : str
    full_article_text : str
    summary : Optional[str] = None
    topics : Optional[List[str]] = None

    def basic_info(self) -> dict[str, Any]:
        return{
            "title" : self.title,
            "url" : self.url,
            "category": self.category,
            "full_article_text" : self.full_article_text
        }
    

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Article":
        return cls(**data)


    def __repr__(self):
        return f"""Title: {self.title}
        URL: {self.url}
        Category: {self.category}
        FullText: {self.full_article_text}
        """
