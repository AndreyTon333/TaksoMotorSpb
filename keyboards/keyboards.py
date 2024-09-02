from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from database.table import async_session, Stations, Doctors
#from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
#from aiogram.utils.keyboard import InlineKeyboardBuilder

"""
def kb_in_del_station() -> InlineKeyboardMarkup:
    but = InlineKeyboardButton(text=f'Да, удалить выбранный Парк')
                               #callback_data='del_station')
    kb = InlineKeyboardMarkup(inline_keyboard=[[but]])
    return kb
"""

# Кнопки главной клавиатуры
def kb_main() -> ReplyKeyboardMarkup:
    button_1 = KeyboardButton(text='РАБОТА С ВОДИТЕЛЯМИ (АВТОКОЛОННА)')
    button_2 = KeyboardButton(text='ТЕХНИЧЕСКИЙ ОТДЕЛ (Поломка авто)')
    button_3 = KeyboardButton(text='НОЧНАЯ ТЕХ СЛУЖБА')
    button_4 = KeyboardButton(text='СЕРВИСЫ')
    button_5 = KeyboardButton(text='ДТП')
    button_6 = KeyboardButton(text='ГРАФИК РАБОТЫ ПАРКА')
    button_7 = KeyboardButton(text='Путевой лист "Креативные решения" (образец)')
    button_8 = KeyboardButton(text='МЕДИКИ')
    button_9 = KeyboardButton(text='ТАБЛИЦА ШТРАФОВ')
    button_10 = KeyboardButton(text='Гос. тех. осмотр')
    button_11 = KeyboardButton(text='МЕТАН')
    button_admin = KeyboardButton(text='Перейти в режим "Администратор"')

    keybord = ReplyKeyboardMarkup(
        keyboard=[[button_1], [button_2], [button_3],
            [button_4, button_5],
            [button_6], [button_7],
            [button_8, button_9],
            [button_10, button_11],
            [button_admin]
        ], resize_keyboard=True
    )
    return keybord

button_back = KeyboardButton(text='🔙 Назад')
button_mane_menu = KeyboardButton(text='🔝 Главное Меню')

kb_main_one_button = ReplyKeyboardMarkup(keyboard=[[button_mane_menu]], resize_keyboard=True)

# Динамическая клавиатера из названий Станций
def kb_b_stations (stations: list) -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()
    buttons: list[KeyboardButton] = [
            KeyboardButton(text=f'{station}') for station in stations]
    kb_builder.row(*buttons, width=2)
    kb_builder.row(button_back, button_mane_menu)
    return kb_builder.as_markup()

# Динамическая клавиатура из названий пунктов Медосмотра
def kb_b_doctors (doctors: list) -> ReplyKeyboardMarkup:
    kb_b = ReplyKeyboardBuilder()
    buttons: list[KeyboardButton] = [
        KeyboardButton(text=f'{doctor}') for doctor in doctors
    ]
    kb_b.row(*buttons, width=2)
    kb_b.row(button_mane_menu)
    return kb_b.as_markup()

# Динамическая клавиатера из названий Станций для удаления
def kb_b_del_stations (stations: list) -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()
    buttons: list[KeyboardButton] = [
            KeyboardButton(text=f'{station}') for station in stations]
    kb_builder.row(*buttons, width=2)
    kb_builder.row(button_mane_menu)
    return kb_builder.as_markup()


# Переход в режим администрирования при нажатии на кнопку 'Перейти в режим "Администратор"'
def kb_admin_edit() -> ReplyKeyboardMarkup:
    but1 = KeyboardButton(text="Добавить новый Парк")
    but2 = KeyboardButton(text="Удалить Парк")
    but3 = KeyboardButton(text='Добавить адрес прохождения медосмотра')
    but4 = KeyboardButton(text="Удалить адрес медосмотра")
    #button_stop_admin=KeyboardButton(text='Выйти из режима "Администратор"')
    keybord = ReplyKeyboardMarkup(
        keyboard=[[but1], [but2], [but3], [but4], [button_mane_menu]],
        resize_keyboard=True
    )
    return keybord


# Попытка создать общую функцию
def kb_contact_location_station(text: str) -> ReplyKeyboardMarkup:
    but_1 = KeyboardButton(text=f'Контакты "{text}"')
    but_2 = KeyboardButton(text=f'Локация "{text}"')
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[but_1], [but_2], [button_back, button_mane_menu]],
        resize_keyboard=True
    )
    return keyboard

# Функция при нажатии кнопки "СЕРВИСЫ"
def kbb_servisis() -> ReplyKeyboardMarkup:
    but_1 = KeyboardButton(text='Сервис Таксомотор')
    but_2 = KeyboardButton(text='Шиномонтаж')
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[but_1], [but_2], [button_back, button_mane_menu]],
        resize_keyboard=True
    )
    return keyboard

# клавиатура с одной кнопкой "Да, удалить этот пункт медосмотра из БД"
but_del_doctor = KeyboardButton(text="Да, удалить этот пункт медосмотра из БД")
kb_del_doctor = ReplyKeyboardMarkup(keyboard=[[but_del_doctor]], resize_keyboard=True)

# клавиатура с одной кнопкой "Да, удалить эту стацию из Базы Данных"
but_del_station = KeyboardButton(text="Да, удалить этот Парк из Базы Данных")
kb_del_station = ReplyKeyboardMarkup(keyboard=[[but_del_station]], resize_keyboard=True)


# Словарь с адресами МЕДИКОВ
"""
dict_medik: dict[str, str] = {'bolshevikov': 'Пр. Большевиков д.42 к.2',
                              'cofiskay': 'Ул. Софийская д.93',
                              '2_Luch': 'Ул. 2-й Луч д.13',
                              'gagarin_34': 'Пр. Ю.Гагарина д.34, к.3, лит. В',
                              'sikeyros': 'Ул. Сикейроса д.1',
                              'gagarin_2': 'Пр. Ю.Гагарина д.2Б',
                              'domostroitelnaya': 'Ул.Домостроительная д.12',
                              'trefoleva': 'Ул. Трефолева д.4, к.1'}
"""
