#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Parsing prices from 15-58m11.ru website and writing them to CSV
# Written by Snownoise
# Snownoise@gmail.com
# 1.0
# 2017-06-25


from bs4 import BeautifulSoup
from bs4 import element
import requests
import csv
import re

import m11_bot_config


def parce_tables(tables):
    temp_prices = []
    for table in tables:
        # one instance of table have complete set for one direction, like КЛИН (89-й км) - МОСКВА
        dir_from = None
        dir_to = None
        price_row = []
        for line in table:

            # Droping NavigableString we don't need
            if not type(line) == element.NavigableString:
                price = None
                directions = None

                try:
                    clean_line = line.contents[0]
                except KeyError:
                    pass

                price = regex_price.findall(clean_line)
                if price:
                    price_row.append(price[0].strip())

                directions = regex_direction.findall(clean_line)
                if directions:
                    dir_from = directions[0][0].strip()
                    dir_to = directions[0][1].strip()
                    price_row.append(locations[dir_from])
                    price_row.append(locations[dir_to])

        temp_prices.append(price_row)
    return temp_prices




prices_transponder = []
prices_cash = []
regex_direction = re.compile('(.+)\s-\s(.+)')
regex_price = re.compile('^\d{2,3}$')

# Dictionary with locations
locations = {
    "МОСКВА": 0,
    "ШЕРЕМЕТЬЕВО-2": 1,
    "ШЕРЕМЕТЬЕВО-1": 2,
    "ЗЕЛЕНОГРАД": 3,
    "МОСКОВСКОЕ МАЛОЕ КОЛЬЦО (A107)": 4,
    "СОЛНЕЧНОГОРСК (пересечение с М10)": 5}

# # SZKK part
# # Loading page and feeding it to BeautifulSoup
page = requests.get(m11_bot_config.price_url_szkk, verify=False)
html = page.text
soup = BeautifulSoup(html, 'html.parser')

# Parcing web page for tables
# Only 'grid1' table is matters (for me) - other ones are for large vehicles
prices_transponder = parce_tables(soup.select("#grid1 .with_transporder.grid__groupitem_ch"))
prices_cash = parce_tables(soup.select("#grid1 .without_transporder.grid__groupitem_ch"))


# # Writing a CSV file with prices (with transponder)
with open(m11_bot_config.price_file_szkk_transponder, 'w', newline='') as csvfile:
    price_writer = csv.writer(csvfile)
    for i in prices_transponder:
        price_writer.writerow(i)

# # Writing a CSV file with prices (without transponder)
with open(m11_bot_config.price_file_szkk_cash, 'w', newline='') as csvfile:
    price_writer = csv.writer(csvfile)
    for i in prices_cash:
        price_writer.writerow(i)
