from dataclasses import dataclass
from typing import Any

@dataclass
class Article:
    title: str
    url: str
    category : str
    full_article_text : str


    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Article":
        return cls(**data)


    def __repr__(self):
        return f"""Title: {self.title}
        URL: {self.url}
        Category: {self.category}
        FullText: {self.full_article_text}
        """
