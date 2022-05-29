import pymysql
import time

from ClientBot import ClientBot

CLIENT_TOKEN = "5567725874:AAGfYLJKKyXk0PJBJ44g8e9M0upTFVYtSwk"
PAYMENT_TOKEN = "1661751239:TEST:719246970"

clientBot = ClientBot(CLIENT_TOKEN, PAYMENT_TOKEN, "localhost", "mydb", "root", "8462")


@clientBot.bot.message_handler(commands=['start'])
def start(message):
    client = {"idtelegram": message.chat.id, "firstname": message.json["chat"].get("first_name", None),
              "secondname": message.json["chat"].get("last_name", None),
              "username": message.json["chat"].get("username", None)}
    clientBot.addclient(client)
    clientBot.start_message(message)

@clientBot.bot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):
    clientBot.bot.answer_shipping_query(shipping_query.id, ok=True,
                                        error_message='Оу, у нас ланч. Спробуйте ще раз через кілька хвилин!')


@clientBot.bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    clientBot.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                            error_message="Відбулась помилка... Спробуйте ще раз.")


@clientBot.bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    clientBot.setpaid(message.json["successful_payment"]["invoice_payload"])
    clientBot.send_message(message,
                           'Ви сплатили замовлення.\n'
                           'Кур’єр доставить вам замовлення! Вартість замовлення :{}'.format(
                               message.successful_payment.total_amount / 100))
    clientBot.start_message(message)


print("starting")
clientBot.start()
print("starting")
#
# con = pymysql.connect(host="localhost", user="root",
#                                    password="8462", database="mydb")
# with con:
#     cur = con.cursor()
#     cur.execute("SELECT * from client;")
#
#     version = cur.fetchall()
#     print("Database version: {}".format(version))