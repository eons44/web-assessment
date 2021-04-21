
import os
import requests
import sys
import logging
import argparse
from urllib.parse import urlparse
from workup import Workup

# logging.basicConfig(level = logging.INFO, format = '%(asctime)s [%(levelname)-8s] - %(message)s (%(filename)s:%(lineno)s)', datefmt = '%H:%M:%S')
logging.basicConfig(level = logging.INFO, format = '%(asctime)s [%(levelname)-8s] - %(message)s', datefmt = '%H:%M:%S')

def eww():
    descriptionStr = "Eons Web Workup gives you detailed feedback on your website."

    parser = argparse.ArgumentParser(description = descriptionStr)
    parser.add_argument('url', type = str, metavar = 'https://example.com', help = 'create a workup for the given url.')

    parser.add_argument('-v', '--verbose', action = 'count', default = 0, dest = 'verbosity')
    parser.add_argument('-l', '--load', help = 'load a links.csv file for further analysis', action = "store_const", const = True, dest = 'load')
    # parser.add_argument('-s', '--save', help = 'save links to a links.csv file', action = "store_const", const = True, dest = 'save') #savehg is done automatically, every time.
    parser.add_argument('-c', '--clone', help = 'save every link that was accessed, as a file.', action = "store_const", const = True, dest = 'clone')
    # parser.add_argument('-a', '--accessibility', help = 'check the site for accessibility issues.', action = "store_const", const = True, dest = 'accessibility') # coming soon.
    # parser.add_argument('-s', '--security', help = 'check the site for security issues.', action = "store_const", const = True, dest = 'security') # coming soon.
    parser.add_argument('-p', '--path', type = str, metavar = './eww/', help = 'choose a custom location for all output.', default = './', dest = 'path')

    args = parser.parse_args()

    if args.verbosity > 0:
        logging.getLogger().setLevel(logging.DEBUG)

    logging.debug("Starting")
    logging.debug(f"url: {args.url}")

    workup = Workup(args.url, args.path)

    if args.load:
        workup.load()

    if args.url is not None:
        logging.info(f"---- starting scan of {workup.root_url} ----")
        workup.assess([workup.root_url], args.clone)
        logging.info("---- done scanning ----")
        logging.info(f"scanned {len(workup.links)}; of those {len([l for l in workup.links if not l.is_broken()])} were broken")

    workup.save()
    logging.info("---- complete ----")
