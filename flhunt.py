#!/usr/bin/env python

import os
import sys
import requests
import lxml.html

# Colors
RESET = "\x1b[0m"
BOLD = "\x1b[1m"
UNDERLINE = "\x1b[4m"

GREEN = "\x1b[0;32m"
WHITE = "\x1b[0;37m"

# Script specifc constants
URL_BASE = "https://freelancehunt.com/projects?"
TAGS = {
    "Parsing": "tags=Парсинг",
    "Python": "skills[]=22",
    # "Java": "skills[]=13",
    "C/C++":  "skills[]=2"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101"
                  "Firefox/61.0",
}


def cprint(fmt, color="", attr="", end="\n", fo=sys.stdout):
    fo.write(color + attr + fmt + RESET + end)

def get_pages_count(url):
    r = requests.get(url, headers=HEADERS)
    root = lxml.html.fromstring(r.text)

    next_pages = root.xpath("//ul[@class='no-padding']/li[@class='']/a/text()")
    for p in next_pages:
        count = int(p)
    return count

def get_current_page(url):
    r = requests.get(url, headers=HEADERS)
    root = lxml.html.fromstring(r.text)

    return int(root.xpath(("//ul[@class='no-padding']/li[@class='active']/"
                           "a/text()"))[0])

def get_titles(url):
    r = requests.get(url, headers=HEADERS)
    root = lxml.html.fromstring(r.text)

    return root.xpath(("//tr[@style='vertical-align: top']/td[@class='left']/"
                      "a[contains(@class, visitable)]/text()"))

def get_tags(url):
    r = requests.get(url, headers=HEADERS)
    root = lxml.html.fromstring(r.text)

    return root.xpath("//tr[@style='vertical-align: top']//div/small/text()")

def get_orders(url):
    return dict(zip(get_titles(url), get_tags(url)))

def main():
    for key in TAGS:
        url = URL_BASE + TAGS[key]

        try:
            curpage = get_current_page(url)
            pages_count = get_pages_count(url)
        except IndexError:
            curpage = 1
            pages_count = curpage

        cprint("\nOrders with tag {}".format(key), color=GREEN, attr=BOLD)
        for p in range(curpage, pages_count + 1, 1):
            print("\nCurrent page {}".format(curpage))
            print("Pages count {}\n".format(pages_count))

            url = URL_BASE + TAGS[key] + "&page=" + str(p)
            for k, v in get_orders(url).items():
                cprint("> {}".format(k), color=WHITE, attr=BOLD)
                cprint("  {attr}{}".format(v, attr=UNDERLINE))

            curpage += 1


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(1)
