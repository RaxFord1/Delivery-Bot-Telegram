import pymysql
import time

from ManagerBot import ManagerBot

CLIENT_TOKEN = "5567725874:AAGfYLJKKyXk0PJBJ44g8e9M0upTFVYtSwk"

managerBot = ManagerBot(CLIENT_TOKEN, "localhost", "mydb", "root", "8462")


@managerBot.bot.message_handler(commands=['start'])
def start(message):
    managerBot.start_message(message)

print("starting")
managerBot.start()
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