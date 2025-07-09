from abc import ABC, abstractmethod

class WebScapper(ABC):
    @abstractmethod
    def scrape(self) -> list[dict]:
        pass