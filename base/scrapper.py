import requests
from bs4 import BeautifulSoup


class BaseScrapper:
    def __init__(self, url: str) -> None:
        self._url: str = url
        self._content: str = None
        self._soup: BeautifulSoup = None

    def _get_content(self) -> None:
        self._content = requests.get(self._url).text

    def _create_soup(self) -> None:
        if not self._content:
            raise ValueError("No content to create soup from.")

        self._soup = BeautifulSoup(self._content, "html.parser")
