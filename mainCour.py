import pymysql
import time

from CourierBot import CourierBot

CLIENT_TOKEN = "5567725874:AAGfYLJKKyXk0PJBJ44g8e9M0upTFVYtSwk"
PAYMENT_TOKEN = "1661751239:TEST:719246970"

courBot = CourierBot(CLIENT_TOKEN,  "localhost", "mydb", "root", "8462")


@courBot.bot.message_handler(commands=['start'])
def start(message):
    courBot.start_message(message)

courBot.my_orders("412435979")
courBot.find_courier('412435979')
courBot.add_courier(1, 1)

print("starting")
courBot.start()
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