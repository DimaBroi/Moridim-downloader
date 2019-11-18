#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, PicklePersistence)
import logging

from globals import Wish_json
from telegramToken import TelegramToken
from wishJsonMgr import WishJsonMgr

logger = logging.getLogger(__name__)
ADD_MEDIA = range(1)

def start(update, contex):
    update.message.reply_text(
        "Hi! I am your bot for Moridim site.\nWhat would you like to download?")
    return ADD_MEDIA


def movie_choice( update, contex):

    name = update.message.text.split(' ', 1)[1]
    if WishJsonMgr().isExist(name):
        return_msg = 'Movie ' + name.upper() + ' already in you wish list'
    else:
        WishJsonMgr().addMovie(name).writeToFile()
        return_msg = 'Movie ' + name.upper() + ' added to monitor'

    update.message.reply_text(return_msg, quote=True)
    return ADD_MEDIA


def series_choice( update, contex):
    try:
        splitted_text = " ".join(update.message.text.split()).split(' ')
        season, episode = splitted_text[-2:]
        name = " ".join(splitted_text[1:-2])

        if WishJsonMgr().isExist(name):
            return_msg = name.upper() + 'already in you wish list'
        else:
            return_msg = name.upper() + ' starting ' + season.upper() + ' ' + episode.upper() + ' added to monitor'
            WishJsonMgr().addSeries(name, int(season[1:]), int(episode[1:])).writeToFile()

    except:
        return_msg = "Your series add request wasn't in the correct format"

    update.message.reply_text(return_msg, quote=True)
    return ADD_MEDIA

def list_choice( update, contex):
    
    wishJsonMgr = WishJsonMgr()
    media_names = wishJsonMgr.getKeys()

    def add_season_episode(name):
        if Wish_json.Keys.series == wishJsonMgr.getType(name):
            name += " S"+str(wishJsonMgr.getSeason(name)).zfill(2) + " E" + str(wishJsonMgr.getEpisode(name)).zfill(2)
        return name

    media_names = list(map(add_season_episode, media_names))
    return_list ='\n'.join([str(n)+". " + name for n, name in zip(list(range(len(media_names))), media_names)])
    update.message.reply_text(return_list)

def done( update, contex):
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("Done adding ! ")
    return ConversationHandler.END


def error( update, contex):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(token=TelegramToken.token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    
    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            ADD_MEDIA: [MessageHandler(Filters.regex(r'^\s*[m|M|movie|Movie].*$'),
                                     movie_choice,
                                     pass_user_data=True),
                        MessageHandler(Filters.regex(r'^\s*[s|S|series|Series]\s+.*\s+[s|S]\d+\s+[e|E]\d+.*$'),
                                     series_choice,
                                     pass_user_data=True),
                        MessageHandler(Filters.regex(r'^\s*[l|L|list|List].*$'),
                                     list_choice,
                                     pass_user_data=True),
                        ],
        },

        fallbacks=[MessageHandler(Filters.regex(r'^Done$'), done, pass_user_data=True)],
        name="my_conversation",
    )

    dp.add_handler(conv_handler)

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
