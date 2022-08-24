import telebot
from telebot import types
import pymysql

# Создаем бота
bot = telebot.TeleBot('TOKEN')

# Команда start
@bot.message_handler(commands=["start"])
def start(m, res=False):

        #обнуление переменных
        global q3Answered
        q3Answered = 0

        #bot.send_poll(m.chat.id, 'вопрос', options=['Почерпнул/а, получал/а информацию по препарату *в этом месяце*', 'Почерпнул/а, получал/а информацию по препарату в прошлом месяце', 'Почерпнул/а, получал/а информацию по препарату в течении полугода (6 месяцев)'])

        #bot.send_poll(m.chat.id, 'вопрос (несколько вариантов ответа)', allows_multiple_answers=True, options=['Почерпнул/а, получал/а информацию по препарату в этом месяце', 'Почерпнул/а, получал/а информацию по препарату в прошлом месяце', 'Почерпнул/а, получал/а информацию по препарату в течении полугода (6 месяцев)'])

        userId = m.from_user.id
        name = m.from_user.first_name
        lastname = m.from_user.last_name
        username = m.from_user.username
        bot.send_message(m.chat.id, "Добрый день, {0}.\n({0},{1},{2}, {3})".format(name, lastname, username, userId))

        q1 = bot.send_message(m.chat.id, 'Сколько пациентов с диагнозом СМА (любого типа) у Вас *НА УЧЕТЕ*? \n(впишите количество человек)', parse_mode = 'Markdown')
        bot.register_next_step_handler(q1, askQ1)


# @bot.poll_answer_handler()
# def handle_poll_answer(pollAnswer):
#     print(pollAnswer)

def askQ1(message):
        chat_id = message.chat.id
        text = message.text
        if not text.isdigit():
                msg = bot.send_message(chat_id, 'Ответ должен быть числом, введите ещё раз.')
                bot.register_next_step_handler(msg, askQ1) #askSource
                return
        q2 = bot.send_message(chat_id, 'Если говорить о последних 2-3 месяцах, __о каких событиях или мероприятиях__, связанных со СМА, Вы слышали', parse_mode = 'Markdown')
        bot.register_next_step_handler(q2, askQ2)

def askQ2(message: types.Message):
        chat_id = message.chat.id
        buttons = [
                types.InlineKeyboardButton(text="1", callback_data="q3_1"),
                types.InlineKeyboardButton(text="2", callback_data="q3_2"),
                types.InlineKeyboardButton(text="3", callback_data="q3_3"),
                types.InlineKeyboardButton(text="4", callback_data="q3_4"),
                types.InlineKeyboardButton(text="5", callback_data="q3_5")
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=5)
        keyboard.add(*buttons)

        q3 = bot.send_message(chat_id, """Пожалуйста, вспомните и укажите, когда Вы последний раз получали информацию (самостоятельно искали, либо Вам её предоставили) по препарату Нусинерсен (Спинраза):\n
1. Почерпнул/а, получал/а информацию по препарату в этом месяце
2. Почерпнул/а, получал/а информацию по препарату в прошлом месяце
3. Почерпнул/а, получал/а информацию по препарату в течении полугода (6 месяцев)
4. Не получал(-а) информации по препарату за последние полгода
5. Ни разу не получал(-а) информацию по препарату
""", reply_markup=keyboard)

q3Answered = 0
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
        global q3Answered
        # Если сообщение из чата с ботом
        if not q3Answered and call.message:
                answ = call.data.split("_")[1]
                answ = "Выбран ответ №" + answ + ".\nСпасибо! Опрос закончен."
                bot.send_message(chat_id=call.message.chat.id, text=answ)    
                q3Answered = True


# Запускаем бота
bot.polling(none_stop=True, interval=0)