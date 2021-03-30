#!/usr/bin/python3

# adapted from https://xtrp.io/blog/2019/11/09/a-quick-python-script-to-find-broken-links/

import requests
import sys
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urljoin

searchedLinks = []
brokenLinks = []
errors = []

def getLinksFromHTML(html):
    def getLink(el):
        return el["href"]
    return list(map(getLink, BeautifulSoup(html, features="html.parser").select("a[href]")))

def findBrokenLinks(domainToSearch, URL, parentURL, outputFile):
    if (not (URL in searchedLinks)) and (not URL.startswith("mailto:")) and (not ("javascript:" in URL)):
        try:
            requestObj = requests.get(URL)
            searchedLinks.append(URL)
            if(requestObj.status_code in [400,404,403,408,409,501,502,503]):
                brokenLinks.append(f"BROKEN ({requestObj.status_code}): {URL} from {parentURL}\n")
                outputFile.write(brokenLinks[-1])
                print(brokenLinks[-1])
            else:
                print(f"okay ({requestObj.status_code}): {URL} from {parentURL}\n")
                if urlparse(URL).netloc == domainToSearch:
                    for link in getLinksFromHTML(requestObj.text):
                        findBrokenLinks(domainToSearch, urljoin(URL, link), URL, outputFile)
        except Exception as e:
            errors.append(f"ERROR: {str(e)}\n")
            outputFile.write(errors[-1])
            print(errors[-1])
            searchedLinks.append(URL)

domain = urlparse(sys.argv[1]).netloc
url = sys.argv[1]
outputFile = open(f"web-assessment_{domain}", "a")
outputFile.write(f"---- starting scan of {domain} ----\n")

findBrokenLinks(domain, url, "", outputFile)

outputFile.write("---- done scanning ----\n\n")
outputFile.write(f"scanned {len(searchedLinks)}; of those {len(brokenLinks)} were broken and {len(errors)} erred\n")
outputFile.write("---- complete ----\n\n")

outputFile.close()
