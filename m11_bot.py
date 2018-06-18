# -*- coding: utf-8 -*-
# Simple telegram bot that shows prices on M11 toll road
# Written by Snownoise
# Snownoise@gmail.com
# 1.0
# 2017-06-25

import m11_bot_config as cfg
import telebot
from telebot import types
import csv
from time import strftime


# Dictionary with locations
locations = {
	0:"МОСКВА (МКАД)",
	1:"ШЕРЕМЕТЬЕВО-2",
	2:"ШЕРЕМЕТЬЕВО-1",
	3:"ЗЕЛЕНОГРАД",
	4:"МОСКОВСКОЕ МАЛОЕ КОЛЬЦО (A107)",
	5:"СОЛНЕЧНОГОРСК (пересечение с М10)"}

# reading prices from CSV
prices = []
with open(cfg.price_file, newline='') as csvfile:
	price_reader = csv.reader(csvfile)
	for row in price_reader:
		tmp_row = []
		for cell in row:
			# Check for numerical values here, exit with error if any non-numerical in file
			try:
				tmp_row.append(int(cell))
			except ValueError:
				print("Error reading numerical values from file ", cfg.price_file)
				exit(1)
				
		# Extra check for length of row. Must be 13 long!
		if len(tmp_row) == 13:
			prices.append(tmp_row)
		else:
			print('Length of row with prices must me exactry 13 elements long.\nSomething must goes wrong')
			exit(1)


		

bot = telebot.TeleBot(cfg.token)

# Default handler for /start and /help commands
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, cfg.help_msg)
	

# Handler for custom buttons with starting location
@bot.message_handler(content_types=["text"])
def send_keyboard(message):
	keyboard = types.InlineKeyboardMarkup()
	button1 = types.InlineKeyboardButton(text = "МКАД", callback_data = "from_mkad")
	button2 = types.InlineKeyboardButton(text = "ШРМ-2", callback_data = "from_svo2")
	button3 = types.InlineKeyboardButton(text = "ШРМ-1", callback_data = "from_svo1")
	button4 = types.InlineKeyboardButton(text = "ЗЕЛ", callback_data = "from_zel")
	button5 = types.InlineKeyboardButton(text = "БЕТ", callback_data = "from_mmk")
	button6 = types.InlineKeyboardButton(text = "СОЛН", callback_data = "from_sol")
	keyboard.add(button1, button2, button3, button4, button5, button6)
	bot.send_message(message.chat.id, "Где вы сейчас?", reply_markup = keyboard)
	

# Handling queries from buttons
@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
	if call.message:
		# Selecting start position depending on pressed button
		if call.data == "from_mkad": start_pos = 0 
		if call.data == "from_svo2": start_pos = 1
		if call.data == "from_svo1": start_pos = 2
		if call.data == "from_zel": start_pos = 3
		if call.data == "from_mmk": start_pos = 4
		if call.data == "from_sol": start_pos = 5
		
		# Getting current date and time
		weekday = int(strftime("%w"))
		hour = int(strftime("%H"))
		
		# Selecting column from the price table
		if hour>=1 and hour<6: col = 2			# 01:00 - 06:00 all days
		if weekday >=1 and weekday <= 4:		# Monday - Thursday
			if hour>=6 and hour<10: col = 3			# 06:00 - 10:00
			if hour>=10 and hour<16: col = 4		# 10:00 - 16:00
			if hour>=16 and hour<=23: col = 5		# 16:00 - 00:00
			if hour>=0 and hour<1: col = 5			# 00:00 - 01:00
		if weekday == 5:						# Friday
			if hour>=6 and hour<10: col = 6			# 06:00 - 10:00
			if hour>=10 and hour<16: col = 7		# 10:00 - 16:00
			if hour>=16 and hour<=23: col = 8		# 16:00 - 00:00
			if hour>=0 and hour<1: col = 8			# 00:00 - 01:00		
		if weekday == 6:						# Saturday
			if hour>=6 and hour<10: col = 9			# 06:00 - 10:00
			if hour>=10 and hour<=23: col = 10		# 10:00 - 00:00
			if hour>=0 and hour<1: col = 10			# 00:00 - 01:00
		if weekday == 0:						# Sunday
			if hour>=6 and hour<10: col = 11		# 06:00 - 10:00
			if hour>=10 and hour<=23: col = 12		# 10:00 - 00:00
			if hour>=0 and hour<1: col = 12			# 00:00 - 01:00
		
		
		# Creating message with prices
		msg_text="ТОЧКА ВЪЕЗДА >>>    " + locations[start_pos] + "\n"
		for row in prices:
			if row[0] == start_pos:
				msg_text = msg_text + locations[row[1]] + ':   ' + str(round(row[col])) + '\n'
		
		# The message will be shown on the same place where buttons were
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg_text)
		
		

# Infinite bot polling	
bot.polling(none_stop=True)
