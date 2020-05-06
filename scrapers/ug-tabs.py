#! /usr/bin/env python
import json
from pathlib import Path
from pprint import pprint
import re

from bs4 import BeautifulSoup
import plac
import requests


def get_tab(url):
    soup = BeautifulSoup(requests.get(url, allow_redirects=True).text, "lxml")
    data = json.loads(soup.select(".js-store")[0]["data-content"])
    tab = re.sub(r"\[/?(tab|ch)\]", "", data["store"]["page"]["data"]["tab_view"]["wiki_tab"]["content"])
    return tab


@plac.annotations(url=("tab url", "positional", None, str, None, "<url>"))
def main(url):
    print(get_tab(url))


if __name__ == "__main__":
    plac.call(main)
