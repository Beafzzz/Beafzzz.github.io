import types

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
import sqlite3
import os

API_TOKEN = '6121275111:AAG88ADXr6Z-ox6R6-CBaC2IyZ8hUhdrnM4'
PAYMENT_TOKEN="1744374395:TEST:0454d218d4ac17867a52"
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

global db
db = sqlite3.connect('menu.db', check_same_thread=False)
cursor = db.cursor()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    await bot.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=types.MenuButtonWebApp(
            text="Веб-приложение", 
            web_app=types.WebAppInfo(url="https://google.com")
        )
    )

    cursor.execute("""CREATE TABLE IF NOT EXISTS shopping_cart(
        id INTEGER PRIMARY KEY,
        user_id UNSIGNED INT,
        user_name TEXT,
        doner_kebab UNSIGNED SMALLINT DEFAULT 0,
        tatmak_pizza UNSIGNED SMALLINT DEFAULT 0,
        shaurma_assorti UNSIGNED SMALLINT DEFAULT 0,
        shaurma_s_sirom UNSIGNED SMALLINT DEFAULT 0,
        shaurma_s_gribami UNSIGNED SMALLINT DEFAULT 0,
        shaurma_s_kartofel_free UNSIGNED SMALLINT DEFAULT 0,
        shaurma_classic UNSIGNED SMALLINT DEFAULT 0,
        shaurma_vegan UNSIGNED SMALLINT DEFAULT 0
        )""")
    db.commit()

    global user_id
    global user_name
    user_id = message.from_user.id
    user_name = message.from_user.username

    cursor.execute("SELECT user_id FROM shopping_cart WHERE user_id = ?",[user_id])
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO shopping_cart(user_id, user_name) VALUES (?,?)",[user_id, user_name])
        db.commit()
        print(f'Зарегестрировано! || {user_id} || {user_name} || (выбор еды)')
    else:
        print(f'Такая запись уже существует! || {user_id} || {user_name} || (выбор еды)')


    cursor.execute("""CREATE TABLE IF NOT EXISTS change_order(
            id INTEGER PRIMARY KEY,
            user_id UNSIGNED INT,
            user_name TEXT,
            meat_cnt UNSIGNED TINYINT DEFAULT 0,
            cheese_cnt UNSIGNED TINYINT DEFAULT 0,
            mush_cnt UNSIGNED TINYINT DEFAULT 0,
            free_cnt UNSIGNED TINYINT DEFAULT 0,
            hot_cnt UNSIGNED TINYINT DEFAULT 0
            )""")
    db.commit()

    cursor.execute("SELECT user_id FROM change_order WHERE user_id = ?", [user_id])
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO change_order(user_id, user_name) VALUES (?,?)", [user_id, user_name])
        db.commit()
        print(f'Зарегестрировано! || {user_id} || {user_name} || (счетчик)')
    else:
        print(f'Такая запись уже существует! || {user_id} || {user_name} || (счетчик)')

    global markup_start
    markup_start = types.InlineKeyboardMarkup(row_width=3)
    btn1 = types.InlineKeyboardButton("📜Меню", callback_data="food_menu")
    btn2 = types.InlineKeyboardButton("🛒Корзина (в разработке)", callback_data="shopping_cart")
    btn3 = types.InlineKeyboardButton("💁О нас", callback_data="address")
    markup_start.add(btn1, btn2, btn3)
    await bot.send_message(message.chat.id,
                     text=f'Здравствуй, {message.from_user.username}. Это телеграмм бот нашего кафе "Колыван"',
                     reply_markup=markup_start)

@dp.callback_query_handler()
async def callback(call: types.CallbackQuery) -> None:
    if call.message:
        if call.data == "food_menu":
            global markup_change
            markup_change = types.InlineKeyboardMarkup(row_width=1)
            change1 = types.InlineKeyboardButton('✅Да', callback_data="yes")
            change2 = types.InlineKeyboardButton('❌Нет', callback_data="no")
            markup_change.add(change1, change2)

            global markup_menu_food
            markup_menu_food = types.InlineKeyboardMarkup(row_width=3)
            btn1 = types.InlineKeyboardButton("🌯Шаурма🌯", callback_data="shaurma")
            btn2 = types.InlineKeyboardButton("🍖Донер кебаб🍖", callback_data="doner_kebab")
            btn3 = types.InlineKeyboardButton("🍕Татмак-пицца🍕", callback_data="tatmak_pizza")
            btn4 = types.InlineKeyboardButton("🏠Домой", callback_data="home")
            markup_menu_food.add(btn1, btn2, btn3, btn4)
            await bot.send_message(call.message.chat.id,
                             text=f'Выберите еду:',
                             reply_markup=markup_menu_food)

        elif call.data == "yes":
            global markup_change_order
            markup_change_order = types.InlineKeyboardMarkup(row_width=3)
            btn1 = types.InlineKeyboardButton("➖", callback_data="meat_minus")
            btn2 = types.InlineKeyboardButton(f"🥩Порция мяса🥩", callback_data="1")
            btn3 = types.InlineKeyboardButton("➕", callback_data="meat_plus")
            btn4 = types.InlineKeyboardButton("➖", callback_data="cheese_minus")
            btn5 = types.InlineKeyboardButton(f"🧀Сыр🧀", callback_data="2")
            btn6 = types.InlineKeyboardButton("➕", callback_data="cheese_plus")
            btn7 = types.InlineKeyboardButton("➖", callback_data="mush_minus")
            btn8 = types.InlineKeyboardButton(f"🍄Грибы🍄", callback_data="3")
            btn9 = types.InlineKeyboardButton("➕", callback_data="mush_plus")
            btn10 = types.InlineKeyboardButton("➖", callback_data="free_minus")
            btn11 = types.InlineKeyboardButton(f"🍟Картофель фри🍟", callback_data="4")
            btn12 = types.InlineKeyboardButton("➕", callback_data="free_plus")
            btn13 = types.InlineKeyboardButton("➖", callback_data="hot_minus")
            btn14 = types.InlineKeyboardButton(f"🌶️Халапеньо🌶️", callback_data="5")
            btn15 = types.InlineKeyboardButton("➕", callback_data="hot_plus")
            btn16 = types.InlineKeyboardButton("🏠Домой", callback_data="home")
            btn17 = types.InlineKeyboardButton("📜Меню", callback_data="food_menu")
            btn18 = types.InlineKeyboardButton("🛒Корзина (в разработке)", callback_data="shopping_cart")
            markup_change_order.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12, btn13,
                                    btn14, btn15, btn16, btn17, btn18)

            global change_order_msg
            change_order_msg = await bot.send_message(call.message.chat.id,
                                "<b>🥩Порция мяса🥩</b> - 60 руб X0\n<b>🧀Сыр🧀</b> - 30 руб X0\n<b>🍄Грибы🍄</b> - 30 руб X0\n<b>🍟Картофель фри🍟</b> - 20 руб X0\n<b>🌶️Халапеньо🌶️</b> - 20 руб X0",
                                parse_mode="html",
                                reply_markup=markup_change_order)

        elif call.data == "no":
            await bot.send_message(call.message.chat.id,
                             text=f'Выберите еду:',
                             reply_markup=markup_menu_food)

        elif call.data == "shaurma":
            markup_shaurma = types.InlineKeyboardMarkup(row_width=3)
            btn1 = types.InlineKeyboardButton("🌯Ассорти🌯", callback_data="shaurma_assorti")
            btn2 = types.InlineKeyboardButton("🧀С сыром🧀", callback_data="shaurma_s_sirom")
            btn3 = types.InlineKeyboardButton("🍄С грибами🍄", callback_data="shaurma_s_gribami")
            btn4 = types.InlineKeyboardButton("🍟С картофелем фри🍟", callback_data="shaurma_s_kartofel_free")
            btn5 = types.InlineKeyboardButton("🌯Классическая🌯", callback_data="shaurma_classic")
            btn6 = types.InlineKeyboardButton("🥬Вегетарианская🥬", callback_data="shaurma_vegan")
            markup_shaurma.add(btn1, btn2, btn3, btn4, btn5, btn6)
            await bot.send_message(call.message.chat.id,
                             text='Выберите вид шаурмы, понравившийся вам:',
                             reply_markup=markup_shaurma)

        elif call.data == "shaurma_assorti":
            await bot.send_message(call.message.chat.id,
                                   "<b>🌯Шаурма ассорти🌯\n \nВ состав входит</b>: \nСочная курица, салат весенний, маринованный красный лук, помидоры, огурцы, сыр, грибы, картофель фри, авторские соусы \n \n<b>💸Цена:</b> 250 руб \n \nХотите что-нибудь добавить в шаурму?",
                                   parse_mode='html',
                                   reply_markup=markup_change)
            if call.data == "yes":
                cursor.execute("UPDATE shopping_cart SET shaurma_assorti=shaurma_assorti+1 WHERE user_id=?", [user_id])
                db.commit()

            elif call.data == "no":
                await bot.send_message(call.message.chat.id,
                                       text=f'Выберите еду:',
                                       reply_markup=markup_menu_food)

        elif call.data == "shaurma_s_sirom":
            cursor.execute("UPDATE shopping_cart SET shaurma_s_sirom=shaurma_s_sirom+1 WHERE user_id=?", [user_id])
            db.commit()
            await bot.send_message(call.message.chat.id,
                             "<b>🧀Шаурма с сыром🧀\n \nВ состав входит</b>: \nСочная курица, салат весенний, помидоры, огурцы, сыр, маринованный красный лук, авторские соусы \n \n<b>💸Цена:</b> 190 руб \n \nХотите что-нибудь добавить в шаурму?",
                             parse_mode='html',
                             reply_markup=markup_change)

        elif call.data == "shaurma_s_gribami":
            cursor.execute("UPDATE shopping_cart SET shaurma_s_gribami=shaurma_s_gribami+1 WHERE user_id=?", [user_id])
            db.commit()
            await bot.send_message(call.message.chat.id,
                             "<b>🍄Шаурма с грибами🍄\n \nВ состав входит</b>: \nСочная курица, салат весенний, маринованный красный лук, помидоры, огурцы, шампиньоны, авторские соусы \n \n<b>💸Цена:</b> 190 руб \n \nХотите что-нибудь добавить в шаурму?",
                             parse_mode='html',
                             reply_markup=markup_change)

        elif call.data == "shaurma_s_kartofel_free":
            cursor.execute("UPDATE shopping_cart SET shaurma_s_kartofel_free=shaurma_s_kartofel_free+1 WHERE user_id=?",
                           [user_id])
            db.commit()
            await bot.send_message(call.message.chat.id,
                             "<b>🍟Шаурма с картофелем фри🍟\n \nВ состав входит</b>: \nСочная курица, салат весенний, маринованный красный лук, помидоры, огурцы, картошка фри, авторские соусы \n \n<b>💸Цена:</b> 180 руб \n \nХотите что-нибудь добавить в шаурму?",
                             parse_mode='html',
                             reply_markup=markup_change)

        elif call.data == "shaurma_classic":
            cursor.execute("UPDATE shopping_cart SET shaurma_classic=shaurma_classic+1 WHERE user_id=?", [user_id])
            db.commit()
            await bot.send_message(call.message.chat.id,
                             "<b>🌯Шаурма классическая🌯\n \nВ состав входит</b>: \nСочная курица, салат весенний, маринованный красный лук, помидоры, огурцы, авторские соусы \n \n<b>💸Цена:</b> 160 руб \n \nХотите что-нибудь добавить в шаурму?",
                             parse_mode='html',
                             reply_markup=markup_change)

        elif call.data == "shaurma_vegan":
            cursor.execute("UPDATE shopping_cart SET shaurma_vegan=shaurma_vegan+1 WHERE user_id=?", [user_id])
            db.commit()
            await bot.send_message(call.message.chat.id,
                             "<b>🥬Шаурма вегетаринаская🥬\n \nВ состав входит</b>: \nСалат весенний, маринованный красный лук, помидоры, огурцы, сыр, грибы, картошка фри, авторские соусы \n \n<b>💸Цена:</b> 180 руб \n \nХотите что-нибудь добавить в шаурму?",
                             parse_mode='html',
                             reply_markup=markup_change)

        elif call.data == "tatmak_pizza":
            cursor.execute("UPDATE shopping_cart SET tatmak_pizza=tatmak_pizza+1 WHERE user_id=?", [user_id])
            db.commit()
            await bot.send_message(call.message.chat.id,
                             "<b>🍕Татмак-пицца🍕\n \nВ состав входит</b>: \nФирменная питта,сочная курица, салат весенний, маринованный красный лук, помидоры, огурцы, авторские соусы \n \n<b>💸Цена:</b> 140 руб \n \nХотите что-нибудь добавить в татмак-пиццу?",
                             parse_mode='html',
                             reply_markup=markup_change)

        elif call.data == "doner_kebab":
            cursor.execute("UPDATE shopping_cart SET doner_kebab = doner_kebab+1 WHERE user_id=?", [user_id])
            db.commit()
            await bot.send_message(call.message.chat.id,
                             "<b>🍖Донер кебаб🍖\n \nВ состав входит</b>: \nСочная курица, салат весенний, помидоры, огурцы, маринованный красный лук, авторские соусы \n \n<b>💸Цена:</b> 200 руб \n \nХотите что-нибудь добавить в донер кебаб?",
                             parse_mode='html',
                             reply_markup=markup_change)

        elif call.data == "home":
            await bot.send_message(call.message.chat.id,
                             text=f'Здравствуй, {user_name}. Это телеграмм бот нашего кафе "Колыван"',
                             reply_markup=markup_start)

        elif call.data == "shopping_cart":
            markup_order = types.InlineKeyboardMarkup(row_width=1)
            btn1 = types.InlineKeyboardButton("✅Заказать", callback_data="order")
            btn2 = types.InlineKeyboardButton("🏠Домой", callback_data="home")
            markup_order.add(btn1, btn2)

            for i in cursor.execute("SELECT * FROM shopping_cart WHERE user_id = ?", [user_id]):
                shop = i
            for i in cursor.execute("SELECT * FROM change_order WHERE user_id =?", [user_id]):
                ordik = i

            global summa_zakaza
            summa_zakaza = 200*shop[3] + 140*shop[4] + 250*shop[5] + 190*shop[6] + 190*shop[7] + 180*shop[8] + 160*shop[9] + 180*shop[10] + 60*ordik[3] + 30*ordik[4] + 30*ordik[5] + 20*ordik[6] +20*ordik[7]

            file_txt = open(f"shopping_cart_{user_id}.txt", "w", encoding="utf-8")
            if shop[3] > 0:
                file_txt.write(f"<b>🍖Донер кебаб🍖</b> X{shop[3]} - {200*shop[3]} руб\n")
            if shop[4] > 0:
                file_txt.write(f"<b>🍕Татмак-пицца🍕</b> X{shop[4]} - {140 * shop[4]} руб\n")
            if shop[5] > 0:
                file_txt.write(f"<b>🌯Шаурма ассорти🌯</b> X{shop[5]} - {250 * shop[5]} руб\n")
            if shop[6] > 0:
                file_txt.write(f"<b>🧀Шаурма с сыром🧀</b> X{shop[6]} - {190 * shop[6]} руб\n")
            if shop[7] > 0:
                file_txt.write(f"<b>🍄Шаурма с грибами🍄</b> X{shop[7]} - {190 * shop[7]} руб\n")
            if shop[8] > 0:
                file_txt.write(f"<b>🍟Шаурма с картофелем фри🍟</b> X{shop[8]} - {180 * shop[8]} руб\n")
            if shop[9] > 0:
                file_txt.write(f"<b>🌯Шаурма классическая🌯</b> X{shop[9]} - {160 * shop[9]} руб\n")
            if shop[10] > 0:
                file_txt.write(f"<b>🥬Шаурма вегетарианская🥬</b> X{shop[10]} - {180 * shop[10]} руб\n")
            file_txt.close()

            shopping_cartik = open(f"shopping_cart_{user_id}.txt", "r", encoding="utf-8")

            if summa_zakaza == 0:
                await bot.send_message(call.message.chat.id,
                                    f"Вы ничего не добавляли в корзину.",
                                    reply_markup=markup_start)
            else:
                await bot.send_message(call.message.chat.id,
                                    f"<b>🛒Ваш заказ🛒:</b>\n\n{shopping_cartik.read()}\n<b>💸Общая сумма заказа💸:</b> {summa_zakaza} руб",
                                    parse_mode='html',
                                    reply_markup=markup_order)
            shopping_cartik.close()

        elif call.data == "order":
            markup_order_pay = types.InlineKeyboardMarkup(row_width=1)
            btn1 = types.InlineKeyboardButton("💳Оплатить", pay=True)
            markup_order_pay.add(btn1)

            await bot.send_invoice(call.message.chat.id,
                                   title='Кафе "Колыван"',
                                   description='Нажмите кнопку "💳Оплатить" для обработки заказа',
                                   provider_token=PAYMENT_TOKEN,
                                   currency="RUB",
                                   prices=[types.LabeledPrice(label="ЗАКАЗ", amount=summa_zakaza*100)],
                                   payload="pay_order",
                                   need_phone_number=False,
                                   need_email=False,
                                   is_flexible=False,
                                   reply_markup=markup_order_pay)

        elif call.data == "address":
            await bot.send_message(call.message.chat.id,
                             "Наш адрес: Московское шоссе, 108")
            await bot.send_location(call.message.chat.id, 54.306793, 48.358335)
            await bot.send_message(call.message.chat.id,
                                   text=f'Здравствуй, {user_name}. Это телеграмм бот нашего кафе "Колыван"',
                                   reply_markup=markup_start)

        elif call.data == "meat_minus":
            cursor.execute("UPDATE change_order SET meat_cnt = meat_cnt-1 WHERE user_id=?", [user_id])
            db.commit()
            for i in cursor.execute("SELECT * FROM change_order"):
                meat_cnt = i[3]
                cheese_cnt=i[4]
                mush_cnt=i[5]
                free_cnt=i[6]
                hot_cnt=i[7]
            await bot.delete_message(call.message.chat.id, change_order_msg.message_id)
            change_order_msg = await bot.send_message(call.message.chat.id,
                                  f"<b>🥩Порция мяса🥩</b> - 60 руб X{meat_cnt}\n<b>🧀Сыр🧀</b> - 30 руб X{cheese_cnt}\n<b>🍄Грибы🍄</b> - 30 руб X{mush_cnt}\n<b>🍟Картофель фри🍟</b> - 20 руб X{free_cnt}\n<b>🌶️Халапеньо🌶️</b> - 20 руб X{hot_cnt}",
                                  parse_mode="html",
                                  reply_markup=markup_change_order)

        elif call.data == "meat_plus":
            cursor.execute("UPDATE change_order SET meat_cnt = meat_cnt+1 WHERE user_id=?", [user_id])
            db.commit()
            for i in cursor.execute("SELECT * FROM change_order"):
                meat_cnt=i[3]
                cheese_cnt=i[4]
                mush_cnt=i[5]
                free_cnt=i[6]
                hot_cnt=i[7]
            await bot.delete_message(call.message.chat.id, change_order_msg.message_id)
            change_order_msg = await bot.send_message(call.message.chat.id,
                                   f"<b>🥩Порция мяса🥩</b> - 60 руб X{meat_cnt}\n<b>🧀Сыр🧀</b> - 30 руб X{cheese_cnt}\n<b>🍄Грибы🍄</b> - 30 руб X{mush_cnt}\n<b>🍟Картофель фри🍟</b> - 20 руб X{free_cnt}\n<b>🌶️Халапеньо🌶️</b> - 20 руб X{hot_cnt}",
                                   parse_mode="html",
                                   reply_markup=markup_change_order)

        elif call.data == "cheese_minus":
            cursor.execute("UPDATE change_order SET cheese_cnt = cheese_cnt-1 WHERE user_id=?", [user_id])
            db.commit()
            for i in cursor.execute("SELECT * FROM change_order"):
                meat_cnt = i[3]
                cheese_cnt=i[4]
                mush_cnt=i[5]
                free_cnt=i[6]
                hot_cnt=i[7]
            await bot.delete_message(call.message.chat.id, change_order_msg.message_id)
            change_order_msg = await bot.send_message(call.message.chat.id,
                                  f"<b>🥩Порция мяса🥩</b> - 60 руб X{meat_cnt}\n<b>🧀Сыр🧀</b> - 30 руб X{cheese_cnt}\n<b>🍄Грибы🍄</b> - 30 руб X{mush_cnt}\n<b>🍟Картофель фри🍟</b> - 20 руб X{free_cnt}\n<b>🌶️Халапеньо🌶️</b> - 20 руб X{hot_cnt}",
                                  parse_mode="html",
                                  reply_markup=markup_change_order)

        elif call.data == "cheese_plus":
            cursor.execute("UPDATE change_order SET cheese_cnt = cheese_cnt+1 WHERE user_id=?", [user_id])
            db.commit()
            for i in cursor.execute("SELECT * FROM change_order"):
                meat_cnt = i[3]
                cheese_cnt=i[4]
                mush_cnt=i[5]
                free_cnt=i[6]
                hot_cnt=i[7]
            await bot.delete_message(call.message.chat.id, change_order_msg.message_id)
            change_order_msg = await bot.send_message(call.message.chat.id,
                                  f"<b>🥩Порция мяса🥩</b> - 60 руб X{meat_cnt}\n<b>🧀Сыр🧀</b> - 30 руб X{cheese_cnt}\n<b>🍄Грибы🍄</b> - 30 руб X{mush_cnt}\n<b>🍟Картофель фри🍟</b> - 20 руб X{free_cnt}\n<b>🌶️Халапеньо🌶️</b> - 20 руб X{hot_cnt}",
                                  parse_mode="html",
                                  reply_markup=markup_change_order)

        elif call.data == "mush_minus":
            cursor.execute("UPDATE change_order SET mush_cnt = mush_cnt-1 WHERE user_id=?", [user_id])
            db.commit()
            for i in cursor.execute("SELECT * FROM change_order"):
                meat_cnt = i[3]
                cheese_cnt=i[4]
                mush_cnt=i[5]
                free_cnt=i[6]
                hot_cnt=i[7]
            await bot.delete_message(call.message.chat.id, change_order_msg.message_id)
            change_order_msg = await bot.send_message(call.message.chat.id,
                                  f"<b>🥩Порция мяса🥩</b> - 60 руб X{meat_cnt}\n<b>🧀Сыр🧀</b> - 30 руб X{cheese_cnt}\n<b>🍄Грибы🍄</b> - 30 руб X{mush_cnt}\n<b>🍟Картофель фри🍟</b> - 20 руб X{free_cnt}\n<b>🌶️Халапеньо🌶️</b> - 20 руб X{hot_cnt}",
                                  parse_mode="html",
                                  reply_markup=markup_change_order)

        elif call.data == "mush_plus":
            cursor.execute("UPDATE change_order SET mush_cnt = mush_cnt+1 WHERE user_id=?", [user_id])
            db.commit()
            for i in cursor.execute("SELECT * FROM change_order"):
                meat_cnt = i[3]
                cheese_cnt=i[4]
                mush_cnt=i[5]
                free_cnt=i[6]
                hot_cnt=i[7]
            await bot.delete_message(call.message.chat.id, change_order_msg.message_id)
            change_order_msg = await bot.send_message(call.message.chat.id,
                                  f"<b>🥩Порция мяса🥩</b> - 60 руб X{meat_cnt}\n<b>🧀Сыр🧀</b> - 30 руб X{cheese_cnt}\n<b>🍄Грибы🍄</b> - 30 руб X{mush_cnt}\n<b>🍟Картофель фри🍟</b> - 20 руб X{free_cnt}\n<b>🌶️Халапеньо🌶️</b> - 20 руб X{hot_cnt}",
                                  parse_mode="html",
                                  reply_markup=markup_change_order)

        elif call.data == "free_minus":
            cursor.execute("UPDATE change_order SET free_cnt = free_cnt-1 WHERE user_id=?", [user_id])
            db.commit()
            for i in cursor.execute("SELECT * FROM change_order"):
                meat_cnt = i[3]
                cheese_cnt=i[4]
                mush_cnt=i[5]
                free_cnt=i[6]
                hot_cnt=i[7]
            await bot.delete_message(call.message.chat.id, change_order_msg.message_id)
            change_order_msg = await bot.send_message(call.message.chat.id,
                                  f"<b>🥩Порция мяса🥩</b> - 60 руб X{meat_cnt}\n<b>🧀Сыр🧀</b> - 30 руб X{cheese_cnt}\n<b>🍄Грибы🍄</b> - 30 руб X{mush_cnt}\n<b>🍟Картофель фри🍟</b> - 20 руб X{free_cnt}\n<b>🌶️Халапеньо🌶️</b> - 20 руб X{hot_cnt}",
                                  parse_mode="html",
                                  reply_markup=markup_change_order)

        elif call.data == "free_plus":
            cursor.execute("UPDATE change_order SET free_cnt = free_cnt+1 WHERE user_id=?", [user_id])
            db.commit()
            for i in cursor.execute("SELECT * FROM change_order"):
                meat_cnt = i[3]
                cheese_cnt=i[4]
                mush_cnt=i[5]
                free_cnt=i[6]
                hot_cnt=i[7]
            await bot.delete_message(call.message.chat.id, change_order_msg.message_id)
            change_order_msg = await bot.send_message(call.message.chat.id,
                                  f"<b>🥩Порция мяса🥩</b> - 60 руб X{meat_cnt}\n<b>🧀Сыр🧀</b> - 30 руб X{cheese_cnt}\n<b>🍄Грибы🍄</b> - 30 руб X{mush_cnt}\n<b>🍟Картофель фри🍟</b> - 20 руб X{free_cnt}\n<b>🌶️Халапеньо🌶️</b> - 20 руб X{hot_cnt}",
                                  parse_mode="html",
                                  reply_markup=markup_change_order)

        elif call.data == "hot_minus":
            cursor.execute("UPDATE change_order SET hot_cnt = hot_cnt-1 WHERE user_id=?", [user_id])
            db.commit()
            for i in cursor.execute("SELECT * FROM change_order"):
                meat_cnt = i[3]
                cheese_cnt=i[4]
                mush_cnt=i[5]
                free_cnt=i[6]
                hot_cnt=i[7]
            await bot.delete_message(call.message.chat.id, change_order_msg.message_id)
            change_order_msg = await bot.send_message(call.message.chat.id,
                                  f"<b>🥩Порция мяса🥩</b> - 60 руб X{meat_cnt}\n<b>🧀Сыр🧀</b> - 30 руб X{cheese_cnt}\n<b>🍄Грибы🍄</b> - 30 руб X{mush_cnt}\n<b>🍟Картофель фри🍟</b> - 20 руб X{free_cnt}\n<b>🌶️Халапеньо🌶️</b> - 20 руб X{hot_cnt}",
                                  parse_mode="html",
                                  reply_markup=markup_change_order)

        elif call.data == "hot_plus":
            cursor.execute("UPDATE change_order SET hot_cnt = hot_cnt+1 WHERE user_id=?", [user_id])
            db.commit()
            for i in cursor.execute("SELECT * FROM change_order"):
                meat_cnt = i[3]
                cheese_cnt=i[4]
                mush_cnt=i[5]
                free_cnt=i[6]
                hot_cnt=i[7]
            await bot.delete_message(call.message.chat.id, change_order_msg.message_id)
            change_order_msg = await bot.send_message(call.message.chat.id,
                                  f"<b>🥩Порция мяса🥩</b> - 60 руб X{meat_cnt}\n<b>🧀Сыр🧀</b> - 30 руб X{cheese_cnt}\n<b>🍄Грибы🍄</b> - 30 руб X{mush_cnt}\n<b>🍟Картофель фри🍟</b> - 20 руб X{free_cnt}\n<b>🌶️Халапеньо🌶️</b> - 20 руб X{hot_cnt}",
                                  parse_mode="html",
                                  reply_markup=markup_change_order)

@dp.pre_checkout_query_handler()
async def pre_checkot_query(pre_checkot_q: types.Message):
    await bot.answer_pre_checkout_query(pre_checkot_q.id, ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def succesful_payment(message: types.Message):
    print("SUCCESFUL PAYMENT")
    payment_info = message.successful_payment.to_python()
    print(payment_info)

    if os.path.isfile(f"shopping_cart_{user_id}.txt"):
        os.remove(f"shopping_cart_{user_id}.txt")
        print("File successfully deleted!")

        cursor.execute("UPDATE shopping_cart SET shaurma_assorti = 0 WHERE user_id=?", [user_id])
        db.commit()

        cursor.execute("UPDATE shopping_cart SET shaurma_s_sirom = 0 WHERE user_id=?", [user_id])
        db.commit()

        cursor.execute("UPDATE shopping_cart SET shaurma_s_gribami = 0 WHERE user_id=?", [user_id])
        db.commit()

        cursor.execute("UPDATE shopping_cart SET shaurma_s_kartofel_free = 0 WHERE user_id=?", [user_id])
        db.commit()

        cursor.execute("UPDATE shopping_cart SET shaurma_classic = 0 WHERE user_id=?", [user_id])
        db.commit()

        cursor.execute("UPDATE shopping_cart SET shaurma_vegan = 0 WHERE user_id=?", [user_id])
        db.commit()

        cursor.execute("UPDATE shopping_cart SET doner_kebab = 0 WHERE user_id=?", [user_id])
        db.commit()

        cursor.execute("UPDATE shopping_cart SET tatmak_pizza = 0 WHERE user_id=?", [user_id])
        db.commit()

        cursor.execute("UPDATE change_order SET meat_cnt = 0 WHERE user_id=?", [user_id])
        db.commit()

        cursor.execute("UPDATE change_order SET cheese_cnt = 0 WHERE user_id=?", [user_id])
        db.commit()

        cursor.execute("UPDATE change_order SET mush_cnt = 0 WHERE user_id=?", [user_id])
        db.commit()

        cursor.execute("UPDATE change_order SET free_cnt = 0 WHERE user_id=?", [user_id])
        db.commit()

        cursor.execute("UPDATE change_order SET hot_cnt = 0 WHERE user_id=?", [user_id])
        db.commit()

    else:
        print("File doesn't exists!")

    await bot.send_message(message.chat.id,
                           text=f'✅<b>Заказ был успешно оформлен</b>!✅\n\nНадеемся на дальнейшие заказы от вас, <b>приятного аппетита!</b>',
                           parse_mode="html")
    await bot.send_message(message.chat.id,
                           text=f'Здравствуй, {user_name}. Это телеграмм бот нашего кафе "Колыван"',
                           reply_markup=markup_start)

executor.start_polling(dp)
