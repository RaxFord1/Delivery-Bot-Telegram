from Bot import Bot
import pymysql
import time

from telebot import types

class ManagerBot(Bot):

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
        itembtn1 = types.KeyboardButton('Замовлення')
        itembtn2 = types.KeyboardButton('Курєри')
        itembtn3 = types.KeyboardButton('Клієнти')
        itembtn4 = types.KeyboardButton('Продукти')
        itembtn5 = types.KeyboardButton('Поставки')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)
        self.bot.send_message(message.chat.id, "Як себе маєте?", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.process_start)

    def process_start(self, message):
        markup = types.ReplyKeyboardMarkup(row_width=2)
        if message.json["text"] == "Замовлення":
            itembtn1 = types.KeyboardButton('За останній місяць')
            itembtn2 = types.KeyboardButton('За період')
            itembtn3 = types.KeyboardButton('На сьогодні')
            itembtn4 = types.KeyboardButton('Назад')
            markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
            self.bot.send_message(message.chat.id, "Вы обрали Замовлення", reply_markup=markup)
            self.bot.register_next_step_handler(message, self.process_orders)
        elif message.json["text"] == "Клієнти":
            itembtn1 = types.KeyboardButton('Топ 10')
            itembtn2 = types.KeyboardButton('Все Клієнти')
            itembtn3 = types.KeyboardButton('Назад')
            markup.add(itembtn1, itembtn2, itembtn3)
            self.bot.send_message(message.chat.id, "Вы обрали Клієнти", reply_markup=markup)
            self.bot.register_next_step_handler(message, self.process_clients)
        elif message.json["text"] == "Продукти":
            itembtn1 = types.KeyboardButton('Меньше заданого')
            itembtn2 = types.KeyboardButton('Більше заданого')
            itembtn3 = types.KeyboardButton('Прогноз')
            itembtn4 = types.KeyboardButton('Список')
            itembtn5 = types.KeyboardButton('Назад')
            markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)
            self.bot.send_message(message.chat.id, "Вы обрали Продукти", reply_markup=markup)
            self.bot.register_next_step_handler(message, self.process_products)
        elif message.json["text"] == "Курєри":
            orders = self.couriers()
            self.bot.send_message(message.chat.id, "Курєри:")
            for i in orders:
                txt = "{}, {}, {}".format(i[0], i[1], i[2])
                self.bot.send_message(message.chat.id, txt)
            self.start_message(message)
        elif message.json["text"] == "Поставки":
            orders = self.all_supplies()
            self.bot.send_message(message.chat.id, "Поставки:")
            for i in orders:
                txt = "Продукт: {} Количество: {} ".format(i[0], i[1])
                self.bot.send_message(message.chat.id, txt)
            self.start_message(message)

    def process_clients(self, message):
        if message.json["text"] == "Топ 10":
            orders = self.top_10_clients()
            self.bot.send_message(message.chat.id, "Топ 10 клиентов")
            for i in orders:
                txt = "{}".format(i[0])
                for j in i[1:-1]:
                    txt += " {}".format(j)
                txt += "\nСумма = {}".format(i[-1])
                self.bot.send_message(message.chat.id, str(txt))
            self.start_message(message)
        elif message.json["text"] == "Все Клієнти":
            self.bot.send_message(message.chat.id, "Вы обрали всех клиентов")
            orders = self.all_clients()
            self.bot.send_message(message.chat.id, "Клієнти:")
            for i in orders:
                txt = "{}".format(i[0])
                for j in i[1:-1]:
                    txt += " {}".format(j)
                txt += "\nСумма = {}".format(i[-1])
                self.bot.send_message(message.chat.id, str(txt))
            self.start_message(message)
        elif message.json["text"] == "Назад":
            self.start_message(message)

    def process_products(self, message):
        markup = types.ReplyKeyboardMarkup(row_width=2)
        if message.json["text"] == "Список":
            orders = self.product_list()
            self.bot.send_message(message.chat.id, "Вы обрали Список продуктов:")
            for i in orders:
                txt = "Продукт {}: \n На складе: {}\n Вартість: {} грн.\n".format(i[1], i[4], i[3])
                self.bot.send_message(message.chat.id, txt)
            self.start_message(message)
        elif message.json["text"] == "Прогноз":
            orders = self.products_involved()
            txt = "Прогноз по продуктам:"
            for i in orders:
                self.bot.send_message(message.chat.id, txt)
                txt = "Продукт {}: \n Лишиться: {} \n Задіяно:{}".format(i[0], i[1], i[2])
                self.bot.send_message(message.chat.id, txt)
            self.start_message(message)
        elif message.json["text"] == "Більше заданого":
            self.bot.send_message(message.chat.id, "Введіть число, Більше которого выхотите получить результат",
                             reply_markup=markup)
            self.bot.register_next_step_handler(message, self.more_products)
        elif message.json["text"] == "Меньше заданого":
            self.bot.send_message(message.chat.id, "Введіть число, меньше которого выхотите получить результат",
                             reply_markup=markup)
            self.bot.register_next_step_handler(message, self.less_products)
        elif message.json["text"] == "Назад":
            self.start_message(message)

    def forecast(self):
        with self.con.cursor() as cur:

            cur.execute("select * from `products_involved`")
            row = cur.fetchall()
        return row

    def more_products(self, message):
        if str(message.json["text"]).isdigit():
            products = self.products_more(message.json["text"])
            self.bot.send_message(message.chat.id, "Продукти:")
            for i in products:
                txt = "{}. Количество - {}".format(i[0], i[1])
                self.bot.send_message(message.chat.id, txt)
            self.start_message(message)
        else:
            self.bot.send_message(message.chat.id, "Вы ввели не число. Введіть число!")
            self.bot.register_next_step_handler(message, self.more_products)

    def less_products(self, message):
        if str(message.json["text"]).isdigit():
            products = self.products_less(message.json["text"])
            self.bot.send_message(message.chat.id, "Продукти:")
            for i in products:
                txt = "{}. Количество - {}".format(i[0], i[1])
                self.bot.send_message(message.chat.id, txt)
            self.start_message(message)
        else:
            self.bot.send_message(message.chat.id, "Вы ввели не число. Введіть число!")
            self.bot.register_next_step_handler(message, self.more_products)

    def process_orders(self, message):
        markup = types.ReplyKeyboardMarkup(row_width=2)
        if message.json["text"] == "За останній місяць":
            orders = self.last_month_orders()
            prev_order, n = None, 0
            txt = "Замовлення За останній місяць:"
            for i in orders:
                if not prev_order == i[0]:
                    prev_order = i[0]
                    self.bot.send_message(message.chat.id, txt)
                    txt = "Заказ номер :{}\nВартість: {}".format(n, i[4])
                    txt += "Сплачен" if i[3] == 1 else "Не Сплачен"
                txt += "\n{}. Порцій - {}".format(i[1], i[2])
            self.bot.send_message(message.chat.id, txt)
            self.start_message(message)
        elif message.json["text"] == "За період":
            self.bot.send_message(message.chat.id, "Введіть першу дату YYYY-MM-DD", reply_markup=markup)
            self.bot.register_next_step_handler(message, self.first_period_process)

        elif message.json["text"] == "На сьогодні":
            orders = self.today_orders()
            prev_order, n = None, 0
            txt = "Замовлення на сьогодні:"
            for i in orders:
                if not prev_order == i[0]:
                    prev_order = i[0]
                    self.bot.send_message(message.chat.id, txt)
                    txt = "Заказ номер :{}\nВартість: {}.".format(n, i[4])
                    txt += "Сплачен" if i[3] == 1 else " Не Сплачен"
                txt += "\n{}. Порцій - {}".format(i[1], i[2])
            self.bot.send_message(message.chat.id, txt)
            self.start_message(message)
        elif message.json["text"] == "Назад":
            self.start_message(message)

    def first_period_process(self, message):
        if self.process_date(message.json["text"]) == True:
            self.dates[0] = message.json["text"]
            self.bot.send_message(message.chat.id, "Хорошо, теперь введи вторую дату. \nYYYY-MM-DD")
            self.bot.register_next_step_handler(message, self.second_period_process)
        else:
            self.bot.send_message(message.chat.id, "Ви ввели не правильну другу дату. Спробуйте ще раз. \nYYYY-MM-DD")
            self.bot.register_next_step_handler(message, self.first_period_process)

    def second_period_process(self, message):
        if self.process_date(message.json["text"]) == True:
            self.dates[1] = message.json["text"]
            orders = self.orders_period(self.dates[0], self.dates[1])
            prev_order = None
            n = 0
            txt = "Замовлення с {} по {}:".format(self.dates[0], self.dates[1])
            for i in orders:
                if not prev_order == i[0]:
                    prev_order = i[0]
                    self.bot.send_message(message.chat.id, txt)
                    txt = "Заказ номер :{}\nВартість: {}".format(n, i[3])
                txt += "\n{}. Порцій - {}".format(i[1], i[2])
            self.start_message(message)
        else:
            self.bot.send_message(message.chat.id, "Вы ввели не правильно вторую дату. Спробуйте ще раз. \nYYYY-MM-DD")
            self.bot.register_next_step_handler(message, self.second_period_process)

    def couriers(self):
        with self.con.cursor() as cur:

            cur.execute("select * from courier")
            row = cur.fetchall()
        return row

    def products_involved(self):
        with self.con.cursor() as cur:

            cur.execute("select * from products_involved")
            row = cur.fetchall()
        return row

    def products_more(self,num):
        with self.con.cursor() as cur:

            cur.execute("call producct_overage_on_store({})".format(num))
            row = cur.fetchall()
        return row

    def product_list(self):
        with self.con.cursor() as cur:

            cur.execute("select * from product")
            row = cur.fetchall()
        return row

    def products_less(self,num):
        with self.con.cursor() as cur:

            cur.execute("call producct_lack_on_store({})".format(num))
            row = cur.fetchall()
        return row

    def top_10_clients(self):
        with self.con.cursor() as cur:

            cur.execute("select * FROM view_top_10_clients")
            row = cur.fetchall()
        return row

    def all_clients(self):
        with self.con.cursor() as cur:

            cur.execute("select * FROM view_all_clients")
            row = cur.fetchall()
        return row

    def all_supplies(self):
        with self.con.cursor() as cur:

            cur.execute("select * FROM view_suplies")
            row = cur.fetchall()
        return row

    def process_date(self,date):
        given_time = date
        try:
            time.strptime(given_time, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def last_month_orders(self):
        with self.con.cursor() as cur:

            cur.execute("select * FROM view_last_month_orders")
            row = cur.fetchall()
        return row

    def today_orders(self):
        with self.con.cursor() as cur:

            cur.execute("select * from view_today_orders")
            row = cur.fetchall()
        return row

    def orders_period(self,first_date, second_date):
        with self.con.cursor() as cur:

            cur.execute("call orders_in_period(\'{}\',\'{}\')".format(first_date, second_date))
            row = cur.fetchall()
        return row
