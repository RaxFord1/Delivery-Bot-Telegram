from Bot import Bot

import pymysql
import time

from telebot import TeleBot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, LabeledPrice
from datetime import datetime, timedelta


class ClientBot(Bot):
    orders = {"0": {"id": 0, "num": 0}}
    def __init__(self, token, payment_token, dbHost, dbName, dbUserName, dbPass):
        self.dbHost = dbHost
        self.dbName = dbName
        self.dbUserName = dbUserName
        self.dbPass = dbPass
        self.payment_token = payment_token

        self.con = pymysql.connect(host=self.dbHost, user=dbUserName,
                                   password=self.dbPass, database=self.dbName)
        Bot.__init__(self, token)


    def start_message(self, message):
        markup = types.ReplyKeyboardMarkup(row_width=3)
        itembtn1 = types.KeyboardButton('Замовити')
        itembtn2 = types.KeyboardButton('Мої замовлення')
        markup.add(itembtn1, itembtn2)
        self.send_message(message, "Чого бажаєте?", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.process_start)

    def process_start(self, message):
        markup = types.ReplyKeyboardMarkup(row_width=1)
        if message.json["text"] == "Замовити":
            self.create_order(self.findid(message.chat.id))
            menu = self.getmenu()
            prev_value, n = None, 0
            txt = "Вибери з меню"
            for i in menu:
                if not prev_value == i[0]:
                    prev_value = i[0]
                    self.send_message(message, txt)
                    markup.add(types.KeyboardButton("{}".format(i[1])))
                    n += 1
                    txt = "{}. {}. \nЦіна {}".format(n, i[1], i[3], )
                #txt += "\n {}".format(i[4])
            self.send_message(message, txt, reply_markup=markup)
            self.bot.register_next_step_handler(message, self.process_menu)
        elif message.json["text"] == "Мої замовлення":
            all_orders = self.myorders(self.findid(message.chat.id))
            prev_order = None
            n = 0
            txt = "Твої попередні замовлення:"
            for i in all_orders:
                if not prev_order == i[0]:
                    prev_order = i[0]
                    self.send_message(message, txt)
                    txt = "Заказ номер :{}\nВартість: {}".format(n, i[2])
                txt += "\n{}. Порцій - {}".format(i[1], i[3])
            self.start_message(message)

    def process_menu(self, message):
        markup = types.ReplyKeyboardMarkup()
        text = message.json["text"]
        for i in self.getmenu():
            if i[1] == text:
                self.orders[str(message.chat.id)] = {"id": i[0], "num": 0, "name": i[1]}
                break
        self.send_message(message, "Скільки бажаєте порцій?", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.choose_number)

    def getmenu(self):
        with self.con.cursor() as cur:
            cur.execute("select * from view_menu ")
            row = cur.fetchall()
            return row

    def choose_number(self, message):
        markup = types.ReplyKeyboardMarkup()
        if message.json["text"].isdigit():
            ID = self.findid(message.chat.id)
            print(self.maxorder(ID), self.orders[str(message.chat.id)]["id"], int(message.json["text"]))
            maxord = self.maxorder(ID)
            if maxord is None:
                self.addorder(ID)
                maxord = self.maxorder(ID)
            self.ordersetdish(self.maxorder(ID), self.orders[str(message.chat.id)]["id"], int(message.json["text"]))
            if self.choose_agreement(message):
                self.little_comfirm(message)
            else:
                self.order_agreement(message)
        else:
            self.send_message(message, "Треба відправити число! Скільки бажаєте порцій?", reply_markup=markup)
            self.bot.register_next_step_handler(message, self.choose_number)

    def little_comfirm(self, message):
        markup = types.ReplyKeyboardMarkup()
        itembtn1 = types.KeyboardButton('Оформити замовлення')
        itembtn2 = types.KeyboardButton('Замовити ще страву')
        itembtn3 = types.KeyboardButton('Змінити кількість порцій')
        itembtn4 = types.KeyboardButton('Відмінити замовлення')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
        dishinorder = self.whatinorder(self.maxorder(self.findid(message.chat.id)))
        txt = "Ваше замовлення: \n"
        for i in dishinorder:
            txt += "{}, {} порцій.\n".format(i[1], i[2])
        txt += "\nВартість замовлення {}".format(dishinorder[0][0])
        self.send_message(message, txt, reply_markup=markup)
        self.bot.register_next_step_handler(message, self.confirm_order)

    def confirm_order(self, message):
        text = message.json["text"]
        markup = types.ReplyKeyboardMarkup()
        if text == 'Оформити замовлення':
            self.send_message(message, "Введіть дату і Час, коли хочете, щоб прийшло замовлення. Формат: YYYY:MM:DD:HH:MM",
                              reply_markup=markup)
            self.bot.register_next_step_handler(message, self.choose_date)
        elif text == 'Замовити ще страву':
            menu = self.getmenu()
            prev_value, n = None, 0
            txt = "Вибери з меню"
            for i in menu:
                if not prev_value == i[0]:
                    prev_value = i[0]
                    self.send_message(message,
                                      txt)
                    markup.add(types.KeyboardButton("{}".format(i[1])))
                    n += 1
                    txt = "{}. {}. \nЦена {}".format(n, i[1], i[3], )
                #txt += "\n {}".format(i[4])
            self.send_message(message,
                              txt, reply_markup=markup)
            self.bot.register_next_step_handler(message, self.process_menu)
        elif text == 'Змінити кількість порцій':
            if len(self.whatinorder(self.maxorder(self.findid(message.chat.id)))) > 1:
                dishinorder = self.whatinorder(self.maxorder(self.findid(message.chat.id)))
                for i in dishinorder:
                    markup.add(types.KeyboardButton("{}".format(i[1])))
                self.send_message(message,
                                  "У какого блюда ты хочешь Змінити кількість порцій?",
                                  reply_markup=markup)
                self.bot.register_next_step_handler(message, self.process_menu)
            else:
                self.send_message(message,
                                  "Сколько пожелаешь порций?", reply_markup=markup)
                self.bot.register_next_step_handler(message, self.choose_number)
        elif text == 'Відмінити замовлення':
            self.delete_order(self.maxorder(self.findid(message.chat.id)))
            self.start_message(message)

    def myorders(self, id_client):
        with self.con.cursor() as cur:
            cur.execute("""select `order`.`idorder`, `dish`.`name`, `order`.`price`, `order_has_dish`.`num` from `order` 
    join `order_has_dish` on `order_has_dish`.`order_idorder` = `order`.`idorder`
    join `dish` on `dish`.`iddish` = `order_has_dish`.`dish_iddish`
    where `order`.`id_client` = {}""".format(id_client))
            rows = cur.fetchall()
            return rows

    def choose_agreement(self, message):
        print(self.get_time(self.maxorder(self.findid(message.chat.id))),
              self.get_place(self.maxorder(self.findid(message.chat.id))))
        if self.get_time(self.maxorder(self.findid(message.chat.id))) is None or self.get_place(
                self.maxorder(self.findid(message.chat.id))) is None:
            return True
        else:
            return False

    def choose_date(self, message):
        markup = types.ReplyKeyboardMarkup()
        given_time = message.json["text"]
        print(given_time)
        try:
            time.strptime(given_time, '%Y:%m:%d:%H:%M')
            self.add_time(self.maxorder(self.findid(message.chat.id)), given_time)
            if self.choose_agreement(message):
                self.send_message(message,
                                  "Добре. Тепер давай оберемо місце, куди прибуде замовлення. Напиши адресу",
                                  reply_markup=markup)
                self.bot.register_next_step_handler(message, self.choose_place)
            else:
                self.order_agreement(message)
        except ValueError:
            self.send_message(message,
                              "Не вірний формат. YYYY:MM:DD:HH:MM \nСпробуйте ще раз.",
                              reply_markup=markup)
            self.bot.register_next_step_handler(message, self.choose_date)

    def choose_place(self, message):
        self.add_place(self.maxorder(self.findid(message.chat.id)), message.json["text"])
        self.order_agreement(message)

    def order_agreement(self, message):
        markup = types.ReplyKeyboardMarkup()
        ID = self.findid(message.chat.id)
        max_order = self.maxorder(self.findid(message.chat.id))
        dishinorder = self.whatinorder(max_order)
        order_time = self.get_time(max_order)
        print(ID, order_time)
        txt = "Чудово. Ваше замовлення:\n"
        for i in dishinorder:
            txt += "{}. Порцій - {}\n".format(i[1], i[2])
        txt += "\nВартість замовлення{}".format(dishinorder[0][0])
        txt += "\nДата:  {}.{}.{}".format(order_time.year, order_time.month, order_time.day)
        txt += "\nЧас: {}:{}".format(order_time.hour, order_time.minute)
        txt += "\nАдреса: {}".format(self.get_place(max_order))
        itembtn1 = types.KeyboardButton('Оформити замовлення')
        itembtn2 = types.KeyboardButton('Замовити ще блюдо')
        itembtn3 = types.KeyboardButton('Змінити кількість порцій')
        itembtn4 = types.KeyboardButton('Змінити дату')
        itembtn5 = types.KeyboardButton('Змінити адресу')
        itembtn6 = types.KeyboardButton('Відмінити замовлення')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6)
        self.send_message(message, txt, reply_markup=markup)
        self.send_message(message, "Оформлюємо замовлення?", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.process_agreement)

    def process_agreement(self, message):
        text = message.json["text"]
        markup = types.ReplyKeyboardMarkup()
        if text == 'Оформити замовлення':
            self.send_payment(message)
        elif text == 'Замовити ще блюдо':
            menu = self.getmenu()
            prev_value, n = None, 0
            txt = "Выбери из меню"
            for i in menu:
                if not prev_value == i[0]:
                    prev_value = i[0]
                    self.send_message(message, txt)
                    markup.add(types.KeyboardButton("{}".format(i[1])))
                    n += 1
                    txt = "{}. {}. \nЦіна {}".format(n, i[1], i[3], )
                #txt += "\n {}".format(i[4])
            self.send_message(message, txt, reply_markup=markup)
            self.bot.register_next_step_handler(message, self.process_menu)
        elif text == 'Змінити кількість порцій':
            dishinorder = self.whatinorder(self.maxorder(self.findid(message.chat.id)))
            for i in dishinorder:
                markup.add(types.KeyboardButton("{}".format(i[1])))
            self.send_message(message,
                              "У якого блюда змінити кількість порцій?", reply_markup=markup)
            self.bot.register_next_step_handler(message, self.process_menu)
        elif text == 'Відмінити замовлення':
            self.delete_order(self.maxorder(self.findid(message.chat.id)))
            self.start_message(message)
        elif text == 'Змінити дату':
            self.send_message(message, "Введіть дату і час, коли хочете, щоб прийшло замовлення! Формат дати: YYYY:MM:DD:HH:MM",
                              reply_markup=markup)
            self.bot.register_next_step_handler(message, self.choose_date)
        elif text == 'Змінити адресу':
            self.send_message(message,
                              "Напиши адресу", reply_markup=markup)
            self.bot.register_next_step_handler(message, self.choose_place)

    def delete_order(self, order_id):
        with self.con.cursor() as cur:
            cur.execute("DELETE FROM `order_has_dish` where `order_has_dish`.`order_idorder` = {}".format(order_id))
            cur.fetchall()
            cur.execute("DELETE FROM `order` where `order`.`idorder` = {}".format(order_id))
            cur.fetchall()
            self.con.commit()

    def send_receipt(self, message):
        markup = types.ReplyKeyboardMarkup(row_width=2)
        self.send_message(message, "Чек", reply_markup=markup)

    def add_time(self, order_id, time):
        time += ":00"
        with self.con.cursor() as cur:
            cur.execute("update `order` set `datetime` = \"{}\" where `order`.`idorder` = {}".format(time, order_id))
            rows = cur.fetchall()
            self.con.commit()

    def get_time(self, id_order):
        with self.con.cursor() as cur:
            cur.execute("select `order`.`datetime` from `order` where `order`.`idorder` = {}".format(id_order))

            rows = cur.fetchall()
            if rows == ():
                return None
            else:
                return rows[0][0]

    def get_place(self, id_order):
        with self.con.cursor() as cur:
            cur.execute("select `order`.`place` from `order` where `order`.`idorder` = {}".format(id_order))

            rows = cur.fetchall()
            return rows[0][0]

    def add_place(self, order_id, place):
        with self.con.cursor() as cur:
            cur.execute("update `order` set `place` = \"{}\" where `order`.`idorder` = {}".format(place, order_id))
            rows = cur.fetchall()
            self.con.commit()

    def lackofproducts(self, num=500):
        with self.con.cursor() as cur:
            cur.execute("call producct_lack_on_store({})".format(num))
            rows = cur.fetchall()
            self.con.commit()
            for row in rows:
                print(row)


    def create_order(self, client_id):
        with self.con.cursor() as cur:
            cur.execute("insert into `order` (`id_client`) values (\"{}\")".format(client_id))
            rows = cur.fetchall()
            self.con.commit()

    def addclient(self, client):
        # client = {"idtelegram":412435979,"firstname":"Dima", "secondname":"test", "username":"name"}

        with self.con.cursor() as cur:
            cur.execute("select * from client where idtelegram = {}".format(client["idtelegram"]))
            row = cur.fetchall()
            print(row)
            if row == ():
                with self.con.cursor() as cur:
                    print(client)
                    cur.execute(
                        "insert into `client` (`idtelegram`, `firstname`, `secondname`, `username`) values ({}, \"{}\", \"{}\", \"{}\")".format(
                            client["idtelegram"], client["firstname"], client["secondname"], client["username"]))
                    asd = cur.fetchall()
                    self.con.commit()
        return row

    # clientBot = {"idtelegram": 412435979, "firstname": "Dima", "secondname": "test", "username": "name"}

    def producctoverageonstore(self, num=500):
        with self.con.cursor() as cur:
            cur.execute("call producct_overage_on_store({})".format(num))
            rows = cur.fetchall()
            self.con.commit()
            for row in rows:
                print(row)

    def productlack(self, num=500):
        with self.con.cursor() as cur:
            cur.execute("call producct_lack({})".format(num))
            rows = cur.fetchall()
            self.con.commit()
            for row in rows:
                print(row)

    def ordersetcourier(self, id_dish, id_courier):
        with self.con.cursor() as cur:
            cur.execute("call order_set_courier({},{})".format(id_dish, id_courier))
            cur.fetchall()
            self.con.commit()

    def ordersetdish(self, id_order, id_dish, num):
        with self.con.cursor() as cur:
            cur.execute("call order_set_dish({}, {}, {})".format(id_order, id_dish, num))
            cur.fetchall()
            self.con.commit()

    def setpaid(self, id_order):
        with self.con.cursor() as cur:
            cur.execute("call set_paid({})".format(id_order))
            cur.fetchall()
            self.con.commit()

    def maxorder(self, id_client):
        with self.con.cursor() as cur:
            cur.execute("""select max(`order`.`idorder`) from `order` 
    where `order`.`id_client` = {}""".format(id_client))
            row = cur.fetchall()
            return row[0][0]

    def whatinorder(self, id_order):
        with self.con.cursor() as cur:
            cur.execute("""select `order`.`price`, `dish`.`name`, `order_has_dish`.`num`, `order`.`idorder`, `dish`.`price` from `order`
    join `order_has_dish` on `order_has_dish`.`order_idorder` = `order`.`idorder`
    join `dish` on `dish`.`iddish` = `order_has_dish`.`dish_iddish` where `order`.`idorder` = {}""".format(id_order))
            return cur.fetchall()

    def addorder(self, idclient):
        with self.con.cursor() as cur:
            cur.execute("insert into `order` (`id_client`) values ({})".format(idclient))
            cur.fetchall()
            self.con.commit()

    def findid(self, client_id):
        with self.con.cursor() as cur:
            cur.execute("select `idclient` from client where `idtelegram` = ({})".format(client_id))
            return cur.fetchall()[0][0]

    def addorchangeinorder(self, id_order, id_dish, new_num):
        with self.con.cursor() as cur:
            cur.execute("select * from order_has_dish where `order_idorder` = {}".format(id_order))
            row = cur.fetchall()
            for i in (row):
                if i[3] == id_dish:
                    print(i)
                    cur.execute("""update `order_has_dish` set `order_has_dish`.`num` = {} 
    where (`order_has_dish`.`order_idorder` = {} 
    and `order_has_dish`.`dish_iddish` = {})""".format(new_num, id_order, id_dish))
                    self.con.commit()
                    return True
            cur.execute("""insert into `order_has_dish` (`order_idorder`, `dish_iddish`, `num`) 
            values ({}, {}, {})""".format(id_order, id_dish, new_num))
            self.con.commit()
            return False

    def send_payment(self, message):
        orders = self.whatinorder(self.maxorder(self.findid(message.chat.id)))
        prices = []
        for i in orders:
            prices.append(LabeledPrice(label='{}'.format(i[1]), amount=int(i[2]) * int(i[4]) * 100))
            payload = "{}".format(i[3])
        prices.append(LabeledPrice(label='Доставка', amount=1))

        start_param = "pay"

        self.bot.send_invoice(
            message.chat.id,
            title="Сплата їжі",
            description="Хочете більше смачної їжі?\nТоді ми завжди раді для вас)",
            invoice_payload=payload,
            provider_token=self.payment_token,
            start_parameter=start_param,
            currency="UAH",
            prices=prices
        )
        self.send_message(message, 'Сплатите чек, щоб отримати замовлення. Якщо ви не хочете спрачувати замовлення, напишіть /start і не сплачуйте заказ у майбутньому.\n')

