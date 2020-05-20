from telegram import ReplyKeyboardMarkup, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
import os


class AutoSelfieBot:
    def __init__(self, token, request_kwargs, model_name):
        # with open(os.path.join(PROJECT_PATH, 'data', 'all_users.json'), 'r') as fp:
        #    temp_dict = json.load(fp)
        #    self.all_users = {int(key): value for key, value in temp_dict.items()}

        # self.model, self.graph = get_model(model_name)  # UNCOMMENT !!!

        updater = Updater(token, request_kwargs=request_kwargs)
        dp = updater.dispatcher
        # dp.add_handler(conv_handler)
        dp.add_handler(CommandHandler('start', self.start))
        dp.add_handler(MessageHandler(Filters.document, self.photos))
        dp.add_handler(MessageHandler(Filters.photo, self.photos))
        dp.add_handler(RegexHandler('(?i).*(хуй|блять|пизда|уебок|ебал|ебать).*', self.bad_words_rus))
        dp.add_handler(RegexHandler('(?i).*(shit|fuck|bitch|asshole|bint|cock|cunt|faggot).*', self.bad_words_eng))
        dp.add_handler(MessageHandler(Filters.text, self.text))
        updater.start_polling()
        updater.idle()

    def start(self, bot, update):
        first_name = update.effective_user.first_name
        update.message.reply_text('Hi {}!'.format(first_name))
        # self.all_users[update.message.chat_id] = {'first_name': first_name}

        custom_keyboard = [['English'], ['Russian']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard)

        q = bot.send_message(chat_id=update.message.chat_id,
                             text="Choose language:",
                             reply_markup=reply_markup)

        # write_log(update)
        # return LANG
        # q = bot.send_message(chat_id=update.message.chat_id,
        #                 text="Please choose language:",
        #                 reply_markup=reply_markup,
        #                resize_keyboard=True)
        # print(q)

    def photos(self, bot, update):
        # Пишем лог
        # write_log(update)
        chat_id = update.message.chat_id
        bot.send_chat_action(chat_id=chat_id, action=ChatAction.UPLOAD_PHOTO)  # добавляем эффект загрузки фото
        # Считываем присланное фото/документ
        # read_photo_doc(bot, update)

        # update.message.reply_photo(photo=bio)
        return True

    def text(self, bot, update):
        chat_id = update.message.chat_id
        if update.message.text == 'English':
            # self.all_users[chat_id]['language'] = 'English'
            update.message.reply_text('You chosed English language')
            # with open(os.path.join(PROJECT_PATH, 'data', 'all_users.json'), 'w') as fp:
            #     json.dump(self.all_users, fp)
            self.default_state(bot, update)
            return True
        elif update.message.text == 'Russian':
            # self.all_users[chat_id]['language'] = 'Russian'
            update.message.reply_text('Ты выбрал Русский язык')
            # with open(os.path.join(PROJECT_PATH, 'data', 'all_users.json'), 'w') as fp:
            #    json.dump(self.all_users, fp)
            self.default_state(bot, update)
            return True
        elif update.message.text == 'Описание':
            update.message.reply_text(
                'Привет! Я умею искать людей на фотографиях. Пришли мне свою фотографию, лучшим форматом является фотография с фронтальной камеры твоего смартфона (т.е. с разрешением 240 x 320 пикселей). В противном случае я изменю размер вашего изображения на 240 х 320')
            return True
        elif update.message.text == 'Github проекта':
            update.message.reply_text('Github бота: https://github.com/DmitriiDenisov/AutoSelfie_bot')
            update.message.reply_text('Github нейронной сети: https://github.com/DmitriiDenisov/faces_picsart')
            return True
        elif update.message.text == 'Автор':
            update.message.reply_text('Автор: @DmitriiDenisov')
            return True
        elif update.message.text == 'Description':
            update.message.reply_text(
                'Hello! I can find people in photos. Send me a picture of you, the best format is a photo from the front camera  of your smartphone (i.e 240 x 320 pixels). Otherwise, I will resize you image to 240 x 320')
            return True
        elif update.message.text == 'Github project':
            update.message.reply_text('Github of bot: https://github.com/DmitriiDenisov/AutoSelfie_bot')
            update.message.reply_text('Github of Neural Network: https://github.com/DmitriiDenisov/faces_picsart')
            return True
        elif update.message.text == 'Author':
            update.message.reply_text('Author: @DmitriiDenisov')
            return True
        # elif update.message.text == 'Инфо сервера':
        #    get_server_info(update)
        # elif update.message.text == 'Server info':
        #    get_server_info(update)
        elif update.message.text.lower() == 'умри':
            update.message.reply_text('Завершаю работу')
            os._exit(-1)
        elif update.message.text.lower() == 'die':
            update.message.reply_text('Finishing work')
            os._exit(-1)

        else:
            update.message.reply_text('Я жду фотографию')

    def bad_words_rus(self, bot, update):
        update.message.reply_text('Не обижай бота!')

    def bad_words_eng(self, bot, update):
        update.message.reply_text('Do not insult the bot!')

    def default_state(self, bot, update):
        # if self.all_users[update.message.chat_id]['language'] == 'Russian':
        #    custom_keyboard = [['Описание', 'Github проекта'], ['Автор', 'Инфо сервера']]
        #    text = "Можешь выбрать действие или прислать фото"
        # else:
        custom_keyboard = [['Description', 'Github project'], ['Author', 'Server info']]
        text = "You can choose an action or send a photo"

        reply_markup = ReplyKeyboardMarkup(custom_keyboard)

        bot.send_message(chat_id=update.message.chat_id,
                         text=text,
                         reply_markup=reply_markup)
