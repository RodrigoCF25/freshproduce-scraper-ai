from dataclasses import dataclass

@dataclass
class Article:
    title: str
    url: str
    category : str
    full_article_text : str

    def __repr__(self):
        return f"""Title: {self.title}
        URL: {self.url}
        Category: {self.category}
        FullText: {self.full_article_text[:50]}
        """
