from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message
from aiogram.fsm.state import State, default_state, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from keyboards.keyboards import kb_b_doctors, kb_main, kb_b_stations, kb_contact_location_station, kbb_servisis, kb_admin_edit, kb_main_one_button #kb_stop_admin
from database.reqests import add_station, get_stations, add_doctor, get_doctors, get_adress_doctor, get_anythink_station
from filters.filter import FilterNameDoctor, FilterNameStation
# from database.reqests import add_station

router = Router()

storage = MemoryStorage()

class FSMback(StatesGroup):
    state_parks = State()
    state_contact_location = State()
    state_servis = State()

class FSM_add_station(StatesGroup):
    state_add_new_park = State()
    state_add_phone = State()
    state_add_adress = State()

    state_add_link_lokation = State()

class FSM_add_doctor(StatesGroup):
    state_add_doctor = State()
    state_add_doctor_adress = State()

# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text='🔝 Главное Меню', reply_markup=kb_main())
    await state.set_state(default_state)

"""
# Этот хэндлер срабатывает при нажатии на кнопку kb_stop_admin "Выйти из режима "Администратор" без сохранения данных"
@router.message(F.text == 'Выйти из режима "Администратор"')
async def process_stop_admin(message: Message, state: FSMContext):
    await state.set_state(default_state)
    await message.answer(text='🔝 Главное Меню', reply_markup=kb_main())
"""

# Этот хэндлер срабатывает при нажатии на button_mane_menu ГЛАВНОЕ МЕНЮ
@router.message(F.text == '🔝 Главное Меню')
async def process_but_menu(message: Message, state: FSMContext):
    await message.answer(text='🔝 Главное Меню', reply_markup=kb_main())
    await state.set_state(default_state)


# Этот хэндлер срабатывает при нажатии на button_back НАЗАД
@router.message(F.text == '🔙 Назад')
async def process_but_menu(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == FSMback.state_parks:
        await process_start_command(message=message, state=state)
    if current_state == FSMback.state_contact_location:
        await process_but_1(message=message, state=state)
    if current_state == FSMback.state_servis:
        await process_start_command(message=message, state=state)


# Этот хэндлер срабатывает при нажатии на button_admin АДМИНИСТРИРОВАНИЕ
@router.message(F.text == 'Перейти в режим "Администратор"')
async def process_administrator(message: Message, state: FSMContext):
    await message.answer(text='Вы перешли в режим администрирования', reply_markup=kb_admin_edit())
    await message.answer(text='Вы можете добавить новый Парк или адрес прохождения Медосмотра в базу данных или удалить их из базы данных.\nИспользуйте кнопки.')


 #Этот хэндлер срабатывает при нажатии на Добавить новый парк
@router.message(F.text == "Добавить новый Парк")
async def add_new_park(message: Message, state: FSMContext):
    await message.answer(text='Напишите название нового Парка', reply_markup=kb_main_one_button)
    await state.set_state(FSM_add_station.state_add_new_park)


# Ввод новго парка, сохранение нового парка, переход в режим ожидания ввода телефона
@router.message(FSM_add_station.state_add_new_park)
async def process_add_new_park(message: Message, state: FSMContext):
    await state.update_data(name_station=message.text)
    current_state = await state.get_data()
    await message.answer(text=f'Отлично! Вы добавили парк: {current_state.get("name_station")} ')
    await state.set_state(FSM_add_station.state_add_phone)
    await message.answer(text='А теперь введите номер телефона', reply_markup=kb_main_one_button)



# Ввод телефона, сохранение телефона, переход в режим сохранения адреса
@router.message(FSM_add_station.state_add_phone)
async def process_add_phone(message: Message, state: FSMContext):
    await state.update_data(phone = message.text)
    current_state = await state.get_data()
    await message.answer(text=f'Отлично! Вы добавили номер телефона: {current_state.get("phone")} ')
    await state.set_state(FSM_add_station.state_add_adress)
    await message.answer(text="А теперь введите адрес Парка", reply_markup=kb_main_one_button)

# Ввод адреса, сохранение адреса, переход в режим коментария к адресу
@router.message(FSM_add_station.state_add_adress)
async def process_add_adress(message: Message, state: FSMContext):
    await state.update_data(adress = message.text)
    current_state = await state.get_data()
    await message.answer(text=f'Отлично! Вы добавили адрес: {current_state.get("adress")} ')
    await state.set_state(FSM_add_station.state_add_link_lokation)
    await message.answer(text='Вставте ссылку на электронную карту с адресом Парка. Для этого скопируйте её, например, в приложении Яндекс.карты', reply_markup=kb_main_one_button)

# Ввод ссылки на карту, сохранение, очистка режима FSM
@router.message(FSM_add_station.state_add_link_lokation)
async def process_add_link_lokation(message: Message, state: FSMContext):
    await state.update_data(link_lokation = message.text)
    data = await state.get_data()
    current_state = {"name_station": data['name_station'], "phone": data['phone'], "adress": data['adress'], "link_lokation": data['link_lokation']}
    await message.answer(text=f'Отлично! Ссылка на карту: {current_state.get('link_lokation')} ')
    await add_station(data=current_state)

    await state.clear()
    await message.answer(text='Данные сохранены.\nВы находитесь в режиме администрирования', reply_markup=kb_admin_edit())



#Этот хэндлер срабатывает при нажатии на кнопку "Добавить адрес прохождения медосмотра"
@router.message(F.text == "Добавить адрес прохождения медосмотра")
async def push_add_new_doctor(message: Message, state: FSMContext):
    await message.answer(text='Напишите краткое название нового маста прохождения медосмотра', reply_markup=kb_main_one_button)
    await state.set_state(FSM_add_doctor.state_add_doctor)

# Ввод нового доктора, сохранение нового доктора, переход в режим ожидания ввода адреса доктора
@router.message(FSM_add_doctor.state_add_doctor)
async def add_new_doctor(message: Message, state: FSMContext):
    await state.update_data(name_doctor=message.text)
    current_state = await state.get_data()
    await message.answer(text=f'Отлично! Вы добавили название нового пункта проведения медосмотра: "{current_state.get('name_doctor')}" ',
                         reply_markup=kb_main_one_button)
    await state.set_state(FSM_add_doctor.state_add_doctor_adress)
    await message.answer(text='А теперь введите адрес прохождения медосмотра')

# Ввод адреса медосмотра, сохранение адреса медосмотра, выход из режима
@router.message(FSM_add_doctor.state_add_doctor_adress)
async def add_new_doctor_adress(message: Message, state: FSMContext):
    await state.update_data(adress_doctor=message.text)
    data = await state.get_data()
    current_state = {"name_doctor": data['name_doctor'], "adress_doctor": data['adress_doctor']}
    await message.answer(text=f'Отлично! Вы добавили адрес нового пункта проведения медосмотра: "{current_state.get('adress_doctor')}" ')
    await add_doctor(data=current_state)
    await state.clear()
    await message.answer(text='Данные сохранены.\nВы находитесь в режиме администрирования', reply_markup=kb_admin_edit())



# Этот хэндлер срабатывает при нажатии на button_1 РАБОТА С ВОДИТЕЛЯМИ (АВТОКОЛОННА)
@router.message(F.text == 'РАБОТА С ВОДИТЕЛЯМИ (АВТОКОЛОННА)')
async def process_but_1(message: Message, state: FSMContext):
    stations = [station for station in await get_stations()]
    await message.answer(text='Выберете парк, где получали автомобили:', reply_markup=kb_b_stations(stations))
    await state.set_state(FSMback.state_parks)


    # Этот хэндлер срабатывает при нажатии  кнопки button_nnn ПАРКИ
#@router.message(lambda x: x.text in ['Кировский завод', 'Маршала Жукова', 'Рыбацкий проезд', 'Оптиков', 'Кубатура', 'Звёздная', 'Кушелевская дорога'])
@router.message(FilterNameStation())
async def process_push_park_button(message: Message, state: FSMContext):
    await message.answer(text=f'Выбрана площадка "{message.text}"', reply_markup=kb_contact_location_station(message.text))
    await state.set_state(FSMback.state_contact_location)

# Этот хэндлер срабатывает при нажатии на but_nnn Контакты "............."

@router.message(lambda message: 'Контакты' in message.text)
async def process_push_contacts(message: Message):
    station = await get_anythink_station(name_station=message.text.split(sep=' ', maxsplit=1)[1].replace('"', ''))
    await message.answer(text=f'{station.phone}')



@router.message(lambda message: 'Локация' in message.text)
async def process_push_contacts(message: Message):
    station = await get_anythink_station(name_station=message.text.split(sep=' ', maxsplit=1)[1].replace('"', ''))
    await message.answer(text=f'{station.adress}\n'
                        f'{station.link_lokation}')




# Этот хэндлер срабатывает при нажатии на button_2 ТЕХНИЧЕСКИЙ ОТДЕЛ (Поломка авто)
@router.message(F.text == 'ТЕХНИЧЕСКИЙ ОТДЕЛ (Поломка авто)')
async def process_button_2(message: Message):
    await message.answer(text=f'Звонки принимаются: с 09:00-18:00\n\n'
                              f'+7952247629 (тех.неисправность)\n\n'
                              f'+7904337942  (тех.неисправность)\n\n'
                              f'+7904556180 (плановое ТО, ГРМ, сезонный шиномонтаж)\n\n'
                              f'После 18:00- сообщение WhatsApp. (гос.номер А/М, ФИО, проблема) Вам перезвонят,в рабочее время.')


   # Этот хэндлер срабатывает при нажатии на button_3 НОЧНАЯ ТЕХ СЛЕЖБА
@router.message(F.text == 'НОЧНАЯ ТЕХ СЛУЖБА')
async def process_button_3(message: Message):
    await message.answer(text='ЗВОНИТЬ С 18:00 ДО 09.00\n\nТЕЛ: +7904556169\nЗВОНИТЬ ПО ТЕХНИЧЕСКИМ ВОПРОСАМ.')


  #Этот хэндлер срабатывает при нажатии на button СЕРВИСЫ
@router.message(F.text == 'СЕРВИСЫ')
async def process_servises(message: Message, state: FSMContext):
    await message.answer(text='СЕРВИСЫ', reply_markup=kbb_servisis())
    await state.set_state(FSMback.state_servis)

@router.message(F.text == 'Сервис Таксомотор')
async def process_servis_taksomotor(message: Message):
    await message.answer_video(video='BAACAgIAAxkBAAICBWbLAbTYGmN3ZiI54joJux6bxAJzAAJXVAAC5UBYSlKPU3JwX0b1NQQ')
    await message.answer(text='https://yandex.ru/navi/10174/saint-petersburg-and-leningrad-oblast/house/polevaya_ulitsa_5b/Z0kYcwdnQUIDQFtjfXR1eXlnZw==/?from=navi&lang=ru&ll=30.507874%2C59.848543&z=16.4')
    await message.answer(text='Полевая улица, 5Б\nдеревня Новосаратовка, Свердловское городское поселение, Всеволожский район, Ленинградская область')
    await message.answer(text='Номер телефона для предварительной записи:\n+7994408913\n\n+7992164328')

@router.message(F.text == 'Шиномонтаж')
async def process_servis_shynomontag(message: Message):
    await message.answer(text=f'Полевая улица, 5Б\n\n'
                         f'https://yandex.ru/navi/10174/saint-petersburg-and-leningrad-oblast/house/polevaya_ulitsa_5b/Z0kYcwdnQUIDQFtjfXR1eXlnZw==/?from=navi&lang=ru&ll=30.507874%2C59.848543&z=16.4')


@router.message(F.text == 'ДТП')
async def process_DTP(message: Message):
    await message.answer(text=f'+7992175999\n\n+7904337943')

@router.message(F.text == 'ГРАФИК РАБОТЫ ПАРКА')
async def process_DTP(message: Message):
    await message.answer(text=f'Понедельник - Пятница с 09:00-18:00\n'
                         f'Суббота (только выдача) с 10:00-17:00\n'
                         f'Воскресенье - ВЫХОДНОЙ')

@router.message(F.text == 'Путевой лист "Креативные решения" (образец)')
async def process_putevoi_list(message: Message):
    await message.answer_photo(photo='AgACAgIAAxkBAAICGWbLCRZmcDKj2qJYvBsLZiT009DdAAJY5zEb5UBYSui78qTOrrsDAQADAgADeQADNQQ')

# этот роутер срабатывает при нажатии на МЕДИКИ
@router.message(F.text == 'МЕДИКИ')
async def process_doctor(message: Message):
    doctors = [doctor for doctor in await get_doctors()]
    await message.answer(text='Выберите пункт прохождения медосмотра:', reply_markup=kb_b_doctors(doctors))

@router.message(FilterNameDoctor())
async def process_doctor_show_adress(message: Message):
    doctor = await get_adress_doctor(name_doctor=message.text)

    await message.answer(text=f'{doctor.adress_doctor}')








#button_8 = KeyboardButton(text='МЕДИКИ')
#button_9 = KeyboardButton(text='ТАБЛИЦА ШТРАФОВ')
#button_10 = KeyboardButton(text='Гос. тех. осмотр')
#button_11 = KeyboardButton(text='МЕТАН')