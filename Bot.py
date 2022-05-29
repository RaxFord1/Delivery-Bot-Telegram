from telebot import TeleBot


class Bot:
    def __init__(self, token):
        self.token = token
        self.bot = TeleBot(self.token)

    def send_message(self, message, text, reply_markup=None):
        if reply_markup is not None:
            self.bot.send_message(message.chat.id, text, reply_markup=reply_markup)
        else:
            self.bot.send_message(message.chat.id, text)
