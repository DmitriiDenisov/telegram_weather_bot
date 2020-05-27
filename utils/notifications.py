from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from utils.constants import d_symbols
from utils.queue import rem_notif, set_notif, notif_func_forecast


def call_notifications_menu(update, context):
    """
    Returns inline keyboard to user
    :param update:
    :param context:
    :param jobQueue:
    :return:
    """
    inline_keyboard = context.user_data['inline_keyboard']
    for notif in context.user_data['notifs']:
        inline_keyboard[notif.hour // 4][notif.hour % 4].text = '✅' + inline_keyboard[notif.hour // 4][
                                                                          notif.hour % 4].text[1:]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    update.message.reply_text(f'I will send you daily weather info based on chosen time', reply_markup=reply_markup)


def notifications_menu(update, context):
    """
    Gets response from user and either removes notification from jobQueue or sets new notification
    Replies to user with updated inline keyboard
    :param update:
    :param context:
    :param jobQueue:
    :param callback_daily:
    :return:
    """
    query = update.callback_query
    query.answer()
    chat_id = update.effective_chat.id
    inline_keyboard = context.user_data['inline_keyboard']
    num = int(query.data)
    new_s = d_symbols[inline_keyboard[num // 4][num % 4].text[0]]
    if new_s == '🛑':
        rem_notif(chat_id, f"{num}:00".zfill(2), context)
    else:
        set_notif(chat_id, f"{num}:00".zfill(2), context, notif_func_forecast)

    inline_keyboard[num // 4][num % 4] = InlineKeyboardButton(f'{new_s}{f"{num}:00".zfill(2)}',
                                                              callback_data=num)

    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    query.edit_message_text(
        text="I will send you daily weather info based on chosen time",
        reply_markup=reply_markup
    )
