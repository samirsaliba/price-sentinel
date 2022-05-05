"""
Run this code to get the ID from your chat on Telegram
So the bot can send messages to this ID in the future

Instructions:
1. Run this script
2. Send /start to your bot - It will reply with your chat-id.
3. Collect and save your chat-id somewhere
4. Store your chat-id in the .env file as 
    TELEGRAM_CHAT_ID="your-chat-id"
5. Stop the script

Done!
Now the PriceSentinel app can send you notifications
via Telegram
"""
import os
from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler

def start(update: Update, context: CallbackContext):
    text = f"""Hello!
    Your chat_id is '{update.effective_chat.id}'
    Please store it in the .env file as
    TELEGRAM_CHAT_ID="your-chat-id"
    Or refer to the docs if you have any doubts.
    You can stop the script to get the ID now :)
    """
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)


if __name__ == '__main__':
    TOKEN = os.environ["TELEGRAM_TOKEN"]

    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    updater.start_polling()
