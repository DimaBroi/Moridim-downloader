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

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, RegexHandler,
                          ConversationHandler)
from imdb import IMDb
import re
import logging
movies = None
logger = logging.getLogger(__name__)

CHOOSE_MOVIE = range(1)
imdb = IMDb()

def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(bot, update):

    update.message.reply_text(
        "Hi! I am your bot for Moridim site.\nWhat would you like to download?")
    return CHOOSE_MOVIE


def movie_choice(bot, update, user_data):
    reply_keyboard = [['Yep', 'No, show next']]
    print(update.message.text)
    movies = imdb.search_movie(update.message.text)
    imdb.update(movies[0], "main")
    update.message.reply_photo(re.sub(r"@\..*", "@._V1_UY536_CR1,0,364,536_AL_.jpg", movies[0]['cover url']),
                               reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return CHOOSE_MOVIE


def series_choice(bot, update, user_data):
    text = update.message.text
    user_data['type'] = text
    update.message.reply_text(
        'What series would you like to download?')

    return ConversationHandler.END

# def custom_choice(bot, update):
#     update.message.reply_text('Alright, please send me the category first, '
#                               'for example "Most impressive skill"')
#
#     return TYPING_CHOICE

#
# def received_information(bot, update, user_data):
#     text = update.message.text
#     category = user_data['choice']
#     user_data[category] = text
#     del user_data['choice']
#
#     update.message.reply_text("Neat! Just so you know, this is what you already told me:"
#                               "{}"
#                               "You can tell me more, or change your opinion on something.".format(
#                                   facts_to_str(user_data)), reply_markup=markup)
#
#     return CHOOSING


def done(bot, update, user_data):
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("I learned these facts about you:"
                              "{}"
                              "Until next time!".format(facts_to_str(user_data)))

    user_data.clear()
    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(token='705834706:AAG2Dmhr8s3riNGj6xVFBx3TT_636BilEOE')#TODO: add to config file

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSE_MOVIE: [RegexHandler('.*',
                                       movie_choice,
                                       pass_user_data=True),
                       RegexHandler('^Series$',
                                    movie_choice,
                                    pass_user_data=True),
                       ],
            #
            # TYPING_CHOICE: [MessageHandler(Filters.text,
            #                                regular_choice,
            #                                pass_user_data=True),
            #                 ],
            #
            # TYPING_REPLY: [MessageHandler(Filters.text,
            #                               received_information,
            #                               pass_user_data=True),
            #                ],
        },

        fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
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