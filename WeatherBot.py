# https://t.me/weather_fcst_bot

import logging
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, Filters, \
    PicklePersistence

from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from utils.constants import LOCATION, CANCEL, NOTIFICATIONS, REPLY_MARKUP, CURRENT_WEATHER, FORECASTS_3_DAYS, \
    FORECASTS_5_DAYS, CHANGE_LOC, TOKENS
from utils.inline_queries import inlinequeries
from utils.locations import location_lat_lon, cancel, location_typing, call_change_location
from utils.notifications import call_notifications_menu, notifications_menu, notif_func_forecast
from utils.queue import recover_queue, rem_notif

from utils.utils import get_current_weather, get_inline_keyboard, get_forecast, send_keyboard

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class WeatherBot:
    def __init__(self, token):
        my_persistence = PicklePersistence(filename='data_storage')
        updater = Updater(token, persistence=my_persistence, use_context=True)
        self.jobQueue = updater.job_queue
        dp = updater.dispatcher

        recover_queue(updater.persistence.user_data, self.jobQueue, notif_func_forecast)

        start_conv = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],

            states={
                LOCATION: [
                    MessageHandler(Filters.location, location_lat_lon),
                    MessageHandler(Filters.text, location_typing)
                ]
            },
            fallbacks=[]
        )
        loc_conv = ConversationHandler(
            entry_points=[MessageHandler(Filters.regex(f'^({CHANGE_LOC})$'), call_change_location)],

            states={
                LOCATION: [
                    MessageHandler(Filters.location, location_lat_lon),
                    MessageHandler(Filters.regex(f'^({CANCEL})$'), cancel),
                    MessageHandler(Filters.text, location_typing)]
            },

            fallbacks=[]
        )
        # Add handlers for location and start
        dp.add_handler(loc_conv)
        dp.add_handler(start_conv)

        # Forecasts menu
        dp.add_handler(
            MessageHandler(Filters.regex(f"^({CURRENT_WEATHER}|{FORECASTS_3_DAYS}|{FORECASTS_5_DAYS})$"),
                           self.forecasts))

        # Notifications
        dp.add_handler(
            MessageHandler(Filters.regex(f'^({NOTIFICATIONS})$'), call_notifications_menu))
        # handler for Notifications inline
        dp.add_handler(CallbackQueryHandler(notifications_menu, pattern='^[0-9]+$'))

        # For inline queries
        dp.add_handler(InlineQueryHandler(inlinequeries))
        # Get for developing purposes
        dp.add_handler(CommandHandler('get', self.get))

        # If do not understand
        dp.add_handler(MessageHandler(Filters.text, self.not_understand))
        # Error handler:
        dp.add_error_handler(self.error)

        # Start pooling
        updater.start_polling()
        updater.idle()

    def start(self, update, context):
        first_name = update.effective_user.first_name
        update.message.reply_text(f'Hi {first_name}!')

        context.user_data['inline_keyboard'] = get_inline_keyboard()
        # remove all existing jobs for thus user
        list_times = context.user_data.get('notifs', [])[:]  # to make a copy
        for t in list_times:
            rem_notif(update.message.chat_id, t.strftime("%H:%M"), context)
        context.user_data['notifs'] = []

        location_keyboard = KeyboardButton(text="📍 Send Location", request_location=True)
        custom_keyboard = [[location_keyboard]]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard)
        update.message.reply_text('Type name of your city or send your location:', reply_markup=reply_markup)
        return LOCATION

    def forecasts(self, update, context):
        if update.message.text == CURRENT_WEATHER:
            get_current_weather(update, context.user_data['location'])
        elif update.message.text == FORECASTS_3_DAYS:
            get_forecast(3, update.message.chat_id, context)
        elif update.message.text == FORECASTS_5_DAYS:
            get_forecast(5, update.message.chat_id, context)
        send_keyboard(update, context)

    def not_understand(self, update, context):
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="I didn't get your request. You can choose an action:",
                                 reply_markup=REPLY_MARKUP)

    def get(self, update, context):
        key = update.message.text.partition(' ')[2]

        value = context.user_data.get(key)
        if value:
            update.message.reply_text(value)
        else:
            update.message.reply_text('Not found')

    def error(self, update, context):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    WeatherBot(token=TOKENS['telegram'])


if __name__ == '__main__':
    main()
