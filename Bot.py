#!/usr/bin/python3
import sys

from telegram.ext import BaseFilter
from telegram.ext import Filters
from telegram import MessageEntity
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler

from HomeBuyingBot import HomeBuyingBot

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    if len(sys.argv) < 2:
        print("Usage {0} <bot_token> <chatroom_id>".format(sys.argv[0]))
        sys.exit(-1)
    token = sys.argv[1]
    chatroom = int(sys.argv[2])
    homeBuyingBot = HomeBuyingBot(token, chatroom)

    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    url_handler = MessageHandler(Filters.entity(MessageEntity.URL), homeBuyingBot.url)
    leaderboard_handler = CommandHandler('leaderboard', homeBuyingBot.getLeaderboard)
    favoriteCommunity_handler = CommandHandler('favoriteCommunity', homeBuyingBot.getFavoriteCommunity)

    dispatcher.add_handler(url_handler)
    dispatcher.add_handler(leaderboard_handler)
    dispatcher.add_handler(favoriteCommunity_handler)

    dispatcher.add_error_handler(print_error_callback)

    updater.start_polling(timeout=30)

def print_error_callback(_, update, error):
    logger = logging.getLogger(__name__)
    logger.error("Exception: {error}, with update {update}".format(error=error, update=update))

main()
