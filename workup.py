
import os
import csv
import logging
from pathlib import Path
from link import Link
from urllib.parse import urlparse

class Workup:
    def __init__(self, root_url, working_dir = "./"):
        self.root_url = root_url
        self.path = working_dir + urlparse(root_url).netloc
        self.links_file = os.path.join(self.path, "links.csv")
        self.clone_path = os.path.join(self.path, "clone")
        self.links = []
        self.follow_schemes = [
            "http:",
            "https:"
        ]

    def assess(self, links = [], clone = True):
        next_links = []
        for url in links:

            # only look at valid urls.
            if not url.startswith(tuple(self.follow_schemes)):
                continue

            # don't duplicate work nor loop.
            if url in [l.url for l in self.links]:
                continue

            logging.debug(f"checking: {url}")

            # do things!
            link = Link(url)

            # try:
            link.get()

            # check result
            if link.is_broken():
                logging.info(f"BROKEN: {link.url}")
            else:
                # graph of all internal edges +1 layer out.
                if link.url.startswith(self.root_url):
                    if clone:
                        link.save(self.clone_path)
                    next_links.append(link.get_links_from_content())

                #keep our memory footprint low.
                link.clear_content()

            # except Exception as e:
            #     logging.error(f"{str(e)}")

            self.links.append(link)

        # recurse
        if next_links:
            self.assess(next_links, clone)

    def save(self):
        logging.debug(f"saving links to {self.links_file}")
        Path(os.path.dirname(self.links_file)).mkdir(parents=True, exist_ok=True)
        file = open(self.links_file, 'w')
        writer = csv.writer(file)
        writer.writerow(['status', 'url'])
        for l in self.links:
            writer.writerow([l.status, l.url])
        file.close
        logging.info(f"links saved to {self.links_file}")

    def load(self):
        logging.debug(f"loading links from {self.links_file}")
        file = open(os.path.join(self.path, "links.csv"), 'r')
        reader = csv.reader(csvfile)
        for count, row in enumerate(reader):
            if not count:
                continue
            link = Link(row[0], row[1])
            self.links.append(link)
        logging.info(f"loaded links from {self.links_file}")
