import re


class TextFormatter:
    @staticmethod
    def clean_text(text: str):
        return re.sub(r'[\xa0\u200b]|\s+', ' ', text).strip()
