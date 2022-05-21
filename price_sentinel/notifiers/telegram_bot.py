"""
To properly setup a Telegram Bot notifier, please refer
to the Telegram documentation on creating bots and 
getting the TOKEN for your bot. It's quite simple
and only requires you to send a message to another Telegram bot
see here: https://core.telegram.org/bots#6-botfather

Then, refer to the utils/telegram_get_chat_id.py script
to get and set your CHAT_ID so the bot can notify you
in the future.
"""
from .base_notifier import BaseNotifier
import os
from telegram.ext import Updater
import textwrap


class TelegramNotifier(BaseNotifier):
    def __init__(self):
        self.TOKEN = os.getenv('TELEGRAM_TOKEN', None)
        self.CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', None)
        self.updater = None

        if None not in (self.TOKEN, self.CHAT_ID):
            self.updater = Updater(token=self.TOKEN, use_context=True)

    def check_setup(self) -> bool:
        return bool(self.updater is not None)

    def close_connection(self):
        self.updater.stop()

    def notify(self, notifications: list):
        if self.check_setup():
            if notifications:
                text = "Hello! New price drops found: \n"
                self.updater.bot.sendMessage(chat_id=self.CHAT_ID,
                                             text=text)

            for notif in notifications:
                product_message = textwrap.dedent(
                    f"""Product [{notif["product_name"]}]
                    - Price: {notif["price"]},
                    - Mean of period: {notif["mean_of_period"]}
                    - Minimum recorded: {notif["historic_min"]}
                    - Retailers with this price: {notif["historic_min"]}
                    """)
                self.updater.bot.sendMessage(chat_id=self.CHAT_ID,
                                             text=product_message)

            self.close_connection()
