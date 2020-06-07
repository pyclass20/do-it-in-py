#!/usr/bin/env python
# coding: utf-8

"""
Download a symbol from Yahoo Finance and ... as CSV
"""
# Created: 06.06.20

import sys
import requests
from bs4 import BeautifulSoup
import json

def url(symbol):
    return(f"https://finance.yahoo.com/quote/{symbol}/history?p={symbol}")


def get(symbol):
    r = requests.get(url(symbol))
    assert r.status_code == 200, f"HTTP {r.status_code}"
    soup = BeautifulSoup(r.text)
    tables = soup.findAll("table", {"data-test": "historical-prices"})
    rows = tables[0].find_all("tr")
    columns = list()
    content = list()
    for i, row in enumerate(rows):
        if i == 0:
            cells = row.find_all("th")
            print("Header", len(cells))
            for cell in cells:
                columns.append(cell.string)
            print(columns)
        else:
            cells = row.find_all("td")
            row_content = dict()
            for i, cell in enumerate(cells):
                row_content[columns[i]] = cell.string
            print(row_content)
            content.append(row_content)
    return(content)


if __name__ == "__main__":
    try:
        symbol = sys.argv[1]
    except Exception:
        symbol = "SAP"

    content = get(symbol)
    x = 15