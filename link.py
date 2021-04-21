
import os
import requests
import logging
from pathlib import Path
from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urlparse

class Link:
    def __init__(self, url = "", status = 0, content = None):
        self.url = url
        self.status = status
        self.content = None

    def get(self):
        self.content = requests.get(self.url)
        self.status = self.content.status_code
        logging.debug(f"[{self.status}] got {self.url}")

    def save(self, base_path = None):
        if not base_path:
            base_path = urlparse(self.url).netloc
        url_path = urlparse(self.url).path
        # folder-like pages need to be saved as files
        if not url_path or url_path[:-1] == "/":
            url_path += "index.html"
        file_path = os.path.join(base_path, url_path)
        Path(os.path.dirname(file_path)).mkdir(parents=True, exist_ok=True)
        file = open(file_path, "w")

        # adjust domain for local use.
        level_str = "../" * (len(url_path.split('/')) - 2)
        root_str = urlparse(self.url).scheme + "://" + urlparse(self.url).netloc
        logging.debug(f"Replacing {root_str} with {level_str}")
        file_content = self.content.text.replace(root_str+'"', level_str+'index.html"')
        file_content = file_content.replace(root_str+'/"', level_str+'index.html"')
        file_content = file_content.replace(root_str+'/', level_str)
        print(file_content)

        file.write(file_content)
        file.close()
        logging.debug(f"saved {file_path}")

    def clear_content(self):
        self.content = None

    def is_broken(self):
        if self.status in [0, 400,404,403,408,409,501,502,503]:
            return True
        return False

    def get_links_from_content(self):
        # logging.debug(f"bs: {[a['href'] for a in BeautifulSoup(self.content.text, parse_only=SoupStrainer('a'), features='html.parser') if a.has_key('href')]}")
        return #[href['href'] for href in BeautifulSoup(self.content.text, parse_only=SoupStrainer('a', 'link', href=True)), features='html.parser')]
