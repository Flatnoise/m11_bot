#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Simple telegram bot that shows prices on M11 toll road
# Written by Snownoise
# Snownoise@gmail.com
# 1.1
# 2019-06-29

import m11_bot_config as cfg
import telebot
from telebot import types
import csv
from time import strftime


# Dictionary with locations
locations = {
    0: "МОСКВА",
    1: "ШЕРЕМЕТЬЕВО-2",
    2: "ШЕРЕМЕТЬЕВО-1",
    3: "ЗЕЛЕНОГРАД",
    4: "МОСКОВСКОЕ МАЛОЕ КОЛЬЦО (A107)",
    5: "СОЛНЕЧНОГОРСК (пересечение с М10)",
    6: "СОЛНЕЧНОГОРСК-3 (67-й км)",
    7: "КЛИН (89-й км)",
    8: "ЯМУГА (97-й км)",
    9: "МОКШИНО (124-й км)",
    10: "ВОСКРЕСЕНСКОЕ (147-й км)"}

# reading prices from CSV
prices = []
with open(cfg.price_file_szkk_transponder, newline='') as csvfile:
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
        if len(tmp_row) == 10:
            prices.append(tmp_row)
        else:
            print('Length of row with prices must me exactry 10 elements long.\nSomething must goes wrong')
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
    button1 = types.InlineKeyboardButton(text="МКАД", callback_data="from_mkad")
    button2 = types.InlineKeyboardButton(text="ШРМ-2", callback_data="from_svo2")
    button3 = types.InlineKeyboardButton(text="ШРМ-1", callback_data="from_svo1")
    button4 = types.InlineKeyboardButton(text="ЗЕЛЕНОГРАД", callback_data="from_zel")
    button5 = types.InlineKeyboardButton(text="БЕТОНКА", callback_data="from_mmk")
    button6 = types.InlineKeyboardButton(text="СОЛ(M10)", callback_data="from_sol")
    # button7 = types.InlineKeyboardButton(text="СОЛ(67КМ))", callback_data="from_sol67")
    # button8 = types.InlineKeyboardButton(text="КЛИН", callback_data="from_klin")
    # button9 = types.InlineKeyboardButton(text="ЯМУГА", callback_data="from_yamuga")
    # button10 = types.InlineKeyboardButton(text="МОКШИНО", callback_data="from_mokshino")
    # button11 = types.InlineKeyboardButton(text="ВОСКРЕСЕНСКОЕ", callback_data="from_voskresenskoye")
#    temporary removed avtodor part of the road - until i write another parcer for it
#    keyboard.add(button1, button2, button3, button4, button5, button6, button7, button8, button10, button11)
    keyboard.add(button1, button2, button3, button4, button5, button6)
    bot.send_message(message.chat.id, "Где вы сейчас?", reply_markup=keyboard)


# Handling queries from buttons
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        # Selecting start position depending on pressed button
        if call.data == "from_mkad": start_pos = 0
        if call.data == "from_svo2": start_pos = 1
        if call.data == "from_svo1": start_pos = 2
        if call.data == "from_zel": start_pos = 3
        if call.data == "from_mmk": start_pos = 4
        if call.data == "from_sol": start_pos = 5
        # if call.data == "from_sol67": start_pos = 6
        # if call.data == "from_klin": start_pos = 7
        # if call.data == "from_yamuga": start_pos = 8
        # if call.data == "from_mokshino": start_pos = 9
        # if call.data == "from_voskresenskoye": start_pos = 10

        # Getting current date and time
        weekday = int(strftime("%w"))
        hour = int(strftime("%H"))

        # Selecting column from the price table
        if hour >= 1 and hour < 6: col = 2          # 01:00 - 06:00 all days
        if weekday >= 1 and weekday <= 4:           # Monday - Thursday
            if hour >= 6 and hour < 14: col = 3       # 06:00 - 14:00
            if hour >= 14 or hour < 1: col = 4        # 14:00 - 01:00
        if weekday == 5:                            # Friday
            if hour >= 6 and hour < 14: col = 5       # 06:00 - 14:00
            if hour >= 14 or hour < 1: col = 6        # 14:00 - 01:00
        if weekday == 6: col = 7                    # Saturday
        if weekday == 0:                            # Sunday
            if hour >= 6 and hour < 14: col = 8       # 06:00 - 14:00
            if hour >= 14 or hour < 1: col = 9        # 14:00 - 01:00


        # Creating message with prices
        msg_text = "ТОЧКА ВЪЕЗДА >>>    " + locations[start_pos] + "\n"
        for row in prices:
            if row[0] == start_pos:
                msg_text = msg_text + locations[row[1]] + ':   ' + str(round(row[col])) + '\n'

        # The message will be shown on the same place where buttons were
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg_text)



# Infinite bot polling
bot.polling(none_stop=True)
