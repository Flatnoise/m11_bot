# Parsing prices from 15-58m11.ru website and writing them to CSV
# Written by Snownoise
# Snownoise@gmail.com
# 1.0
# 2017-06-25


from bs4 import BeautifulSoup
import requests
import csv

import m11_bot_config


prices = []

# Dictionary with locations
locations = {
	"МОСКВА (МКАД)":0,
	"ШЕРЕМЕТЬЕВО-2":1,
	"ШЕРЕМЕТЬЕВО-1":2,
	"ЗЕЛЕНОГРАД":3,
	"МОСКОВСКОЕ МАЛОЕ КОЛЬЦО (A107)":4,
	"СОЛНЕЧНОГОРСК (пересечение с М10)":5}
		

# Loading page and feeding it to BeautifulSoup
page = requests.get(m11_bot_config.price_url)
html = page.text
soup = BeautifulSoup(html, 'html.parser')


# Parcing web page for tables
# Only 'grid1' table is matters (for me) - other ones for large vehicles
tables = soup.select('div[id="grid1"] > table tr')
for table in tables:
	# Selecting rows
	row = table.find_all('td')
	
	# Lenght of row in tariff table must be exactly 12
	if len(row) == 12:
		price_row = []
		for cell in row:
			if not cell.text.isnumeric():
				# Splitting start - destination string into two
				tmp1 = cell.text.strip()
				if tmp1[-2:] == "**":
					tmp1 = tmp1[0:-3]	# Delete ** in the end of the string if present
				indx = tmp1.index(' - ')
				tmp2 = tmp1[0:indx].strip()
				tmp3 = tmp1[indx+3:].strip()
				
				# Write locations into two first elements of the list
				price_row.append(locations[tmp2])
				price_row.append(locations[tmp3])
				
			else:
				# Append a price to the list
				price_row.append(int(cell.text.strip()))
		prices.append(price_row)

# Writing a CSV file with prices
with open(m11_bot_config.price_file, 'w', newline='') as csvfile:
	price_writer = csv.writer(csvfile)
	for i in prices:
		price_writer.writerow(i)

	