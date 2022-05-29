from Bot import Bot

import pymysql
import time

from telebot import TeleBot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, LabeledPrice
from datetime import datetime, timedelta

import pymysql
import time
from telebot import types


class CourierBot(Bot):

    def __init__(self, token, dbHost, dbName, dbUserName, dbPass):
        self.dbHost = dbHost
        self.dbName = dbName
        self.dbUserName = dbUserName
        self.dbPass = dbPass

        self.con = pymysql.connect(host=self.dbHost, user=dbUserName,
                                   password=self.dbPass, database=self.dbName)
        Bot.__init__(self, token)

    def start_message(self, message):
        markup = types.ReplyKeyboardMarkup(row_width=3)
        itembtn1 = types.KeyboardButton('Замовлення на сьогодні')
        itembtn2 = types.KeyboardButton('Взяти замовлення')
        itembtn3 = types.KeyboardButton('Мої замовлення')
        markup.add(itembtn1, itembtn2, itembtn3)
        self.send_message(message, "Які плани на сьогодні?", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.process_start)

    def process_start(self, message):
        markup = types.ReplyKeyboardMarkup(row_width=2)
        if message.json["text"] == "Замовлення на сьогодні":
            orders = self.today_orders()
            prev_order = None
            n = 0
            txt = "Вы обрали замовлення"
            for i in orders:
                if not prev_order == i[0]:
                    prev_order = i[0]
                    self.bot.send_message(message.chat.id, txt)
                    txt = "{}\n{} {} {}\nМісце доставки:{}\nЧас доставки: {}:{}".format(n, i[0], i[1], i[2], i[4],
                                                                                          i[3].hour, i[3].minute)
                txt += "\n {}. Порцій - {}".format(i[5], i[6])
            self.bot.send_message(message.chat.id, txt)
            self.start_message(message)
        elif message.json["text"] == "Взяти замовлення":
            orders = self.today_orders()
            prev_order, n = None, 0
            txt = "Замовлення на сьогодні:"
            for i in orders:
                if not prev_order == i[0]:
                    prev_order = i[0]
                    self.bot.send_message(message.chat.id, txt)
                    markup.add(types.KeyboardButton(i[7]))
                    txt = "{}\n{} {} {}\nМісце доставки:{}\nЧас доставки: {}:{}".format(i[7], i[0], i[1], i[2], i[4],
                                                                                          i[3].hour, i[3].minute)
                txt += "\n {}. Порцій - {}".format(i[5], i[6])
            self.bot.send_message(message.chat.id, txt, reply_markup=markup)
            self.bot.register_next_step_handler(message, self.take_order)
        elif message.json["text"] == "Мої замовлення":
            orders = self.my_orders(message.chat.id)
            prev_order, n = None, 0
            txt = "Яке замовлення ви завершили?"
            if len(orders) == 0:
                self.bot.send_message(message.chat.id, "У вас відсутні замовлення", reply_markup=markup)
                self.start_message(message)
            else:
                for i in orders:
                    prev_order = i[0]
                    self.bot.send_message(message.chat.id, txt)
                    markup.add(types.KeyboardButton(i[5]))
                    txt = "{}\n{} {} {}\nМісце доставки:{}\nЧас доставки: {}:{}".format(i[5], i[0], i[1], i[2], i[4],
                                                                                          i[3].hour, i[3].minute)
                self.bot.send_message(message.chat.id, txt, reply_markup=markup)
                self.bot.register_next_step_handler(message, self.finish_order)


    def finish_order(self, message):
        if str(message.json["text"]).isdigit():
            with self.con.cursor() as cur:

                cur.execute("update `order` set `delivered` = 1 where `idorder` = {}".format(message.json["text"]))
                row = cur.fetchall()
                self.con.commit()
            self.start_message(message)
        else:
            self.bot.send_message(message.chat.id, "Натисніть на кнопку!")
            self.bot.register_next_step_handler(message, self.start_message)

    def take_order(self, message):
        if str(message.json["text"]).isdigit():
            cour_id = self.find_courier(message.chat.id)
            if cour_id == ():
                print(message.chat.id)
                self.bot.send_message(message.chat.id,
                                 "Ви не маєте права робити дану дію. Попросить менеджера додати вас у список кур’єрів!")
            else:
                self.add_courier(cour_id[0][0], message.json["text"])
            self.start_message(message)
        else:
            self.bot.send_message(message.chat.id, "Натисніть на кнопку!")
            self.bot.register_next_step_handler(message, self.start_message)

    def my_orders(self, id_courier):
        with self.con.cursor() as cur:

            cur.execute("call courier_my_orders(\'{}\')".format(id_courier))
            row = cur.fetchall()
            self.con.commit()
        return row

    def find_courier(self,id_courier):
        with self.con.cursor() as cur:

            cur.execute("SELECT `courier`.`id` from `courier` where `courier`.`telegramid` = \'{}\'".format(id_courier))
            row = cur.fetchall()
        return row

    def add_courier(self,courier_id, order_id):
        with self.con.cursor() as cur:

            cur.execute("call order_set_courier({},{})".format(order_id, courier_id))
            cur.fetchall()
            self.con.commit()

    def today_orders(self):
        with self.con.cursor() as cur:

            cur.execute("select * from view_paid_and_without_courier_orders")
            row = cur.fetchall()
        return row