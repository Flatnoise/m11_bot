# -*- coding: utf-8 -*-
# Configuration file for m11_pricebot
token = 'INSERT YOUR BOT TOKEN HERE'

# Адрес списка цен от Северо-западной концессионной компании
price_url_szkk = 'https://15-58m11.ru/trip/grid/'

# Адрес списка цен от Автодора
price_url_avtodor = 'https://www.avtodor-tr.ru/ru/platnye-uchastki/tarify-na-proezd-m-11/'

price_file_szkk_cash = 'prices_szkk_cash.csv'
price_file_szkk_transponder = 'prices_szkk_transponder.csv'
price_file_avtodor_cash = 'prices_avtodor_cash.csv'
price_file_avtodor_transponder = 'prices_avtodor_transponder.csv'
help_msg = """
	Этот бот показывает текущую цену на проезд по платной магистрали М-11
	Цена рассчитывается с учетом транспондера
	Для использования отправьте любой текст
	"""
