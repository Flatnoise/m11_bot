# m11_bot
Simple telegram bot that shows prices on M11 toll road

### Requirements:
- Python3
- pyTelegramBotAPI python package (https://github.com/eternnoir/pyTelegramBotAPI)
- BeautifulSoup python package (https://www.crummy.com/software/BeautifulSoup/)

### Usage:
Edit config m11_bot_config.py: add path to the csv file with prices and you bot's token.
Run m11_parser.py to download current prices from website to csv file. You can put it into cron
When CSV-file with prices is created run m11_bot.py (will work as endless loop). I recommend to run it as service.
