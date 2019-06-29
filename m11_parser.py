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

prices = []
regex_direction = re.compile('(.+)\s-\s(.+)')
regex_price = re.compile('^\d{2,3}$')

# Dictionary with locations
locations = {
    "МОСКВА": 0,
    "ШЕРЕМЕТЬЕВО-2": 1,
    "ШЕРЕМЕТЬЕВО-1": 2,
    "ЗЕЛЕНОГРАД": 3,
    "МОСКОВСКОЕ МАЛОЕ КОЛЬЦО (A107)": 4,
    "СОЛНЕЧНОГОРСК (пересечение с М10)": 5,
    "СОЛНЕЧНОГОРСК-3 (67-й км)": 6,
    "КЛИН (89-й км)": 7,
    "ЯМУГА (97-й км)": 8}

# Loading page and feeding it to BeautifulSoup
page = requests.get(m11_bot_config.price_url, verify=False)
html = page.text
soup = BeautifulSoup(html, 'html.parser')

# Parcing web page for tables
# Only 'grid1' table is matters (for me) - other ones are for large vehicles
tables = soup.select("#grid1 .with_transporder.grid__groupitem_ch")
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

    prices.append(price_row)




    # Selecting rows
    # row = table.find_all('td')

    # # Lenght of row in tariff table must be exactly 12
    # if len(row) == 12:
    #     price_row = []
    #     for cell in row:
    #         if not cell.text.isnumeric():
    #             # Splitting start - destination string into two
    #             tmp1 = cell.text.strip()
    #             if tmp1[-2:] == "**":
    #                 tmp1 = tmp1[0:-3]    # Delete ** in the end of the string if present
    #             indx = tmp1.index(' - ')
    #             tmp2 = tmp1[0:indx].strip()
    #             tmp3 = tmp1[indx + 3:].strip()

    #             # Write locations into two first elements of the list
    #             price_row.append(locations[tmp2])
    #             price_row.append(locations[tmp3])

    #         else:
    #             # Append a price to the list
    #             price_row.append(int(cell.text.strip()))
    #     prices.append(price_row)

# Writing a CSV file with prices
with open(m11_bot_config.price_file, 'w', newline='') as csvfile:
    price_writer = csv.writer(csvfile)
    for i in prices:
        price_writer.writerow(i)

