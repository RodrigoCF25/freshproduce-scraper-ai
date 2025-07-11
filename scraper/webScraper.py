from abc import ABC, abstractmethod

class WebScaper(ABC):
    @abstractmethod
    def scrape(self) -> list[dict]:
        pass