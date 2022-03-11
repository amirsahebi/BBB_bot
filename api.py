#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import telegram


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        "سلام.این ربات جهت دانلود فایل های کلاس های ضبط شده سامانه بیگ بلو باتن ایجاد شده!\n "
        "لطفا لینک کلاس را ارسال کنید،پس از چند دقیقه فایل کلاس برای شما ارسال می شود",
    )


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""

    try:    
        driver = webdriver.Chrome("./chromedriver")
        wait = WebDriverWait(driver, 20)
        driver.get(update.message.text)
        time.sleep(10)
        name=driver.find_element(By.CLASS_NAME,"title").text
        os.system(f"bbb-dl -aw -aa -f ./out.mp4 {update.message.text}")
        os.rename("./out.mp4",f"./{name}.mp4")
        f = open(f'./{name}.mp4', 'rb')
        update.message.reply_video(f)
        os.remove(f'./{name}.mp4')
    except Exception:
        update.message.reply_text('لینک وارد شده صحیح نیست!')

def hello(update, context):
    """Echo the user message."""
    update.message.reply_text("لینک بده آشغال")
    while True:
        print(update.message.text)
        if update.message.text == "HELL":
            update.message.reply_text(update.message.text)
            print(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("5241117890:AAGFsqOE7hrEzsq0XQvBee_3e5R1qW1T6io", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher


    # on different commands - answer in Telegram
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("hello", hello))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()