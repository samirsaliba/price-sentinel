"""
To properly setup a Telegram Bot notifier, please refer
to the Telegram documentation on creating bots and 
getting the TOKEN for your bot. It's quite simple
and only requires you to send a message to another Telegram bot
see here: https://core.telegram.org/bots#6-botfather

Then, refer to the utils/telegram_get_chat_id.py script
to get and set your chat_id so the bot can notify you
in the future.
"""
import os
from telegram.ext import Updater


class TelegramNotifier():
    def __init__(self):
        self.TOKEN = os.getenv('TELEGRAM_TOKEN', None)
        self.CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', None)

        if self.TOKEN is not None \
                and self.CHAT_ID is not None:
            self.updater = Updater(token=self.TOKEN,
                                   use_context=True)

    def notify(self, notifications: list):
        if notifications:
            text = "Hello! New price drops found: \n"
            self.updater.bot.sendMessage(chat_id=self.CHAT_ID,
                                        text=text)

        for notification in notifications:
            product_message = \
                f"""Product [{notification["product_name"]}]
                - Price: {notification["price"]},
                - Mean of period: {notification["mean_of_period"]}
                - Minimum recorded: {notification["historic_min"]}
                - Retailers with this price: {notification["historic_min"]}
                """
            self.updater.bot.sendMessage(chat_id=self.CHAT_ID,
                                         text=product_message)
        self.updater.stop()