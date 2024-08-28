from database.reqests import get_doctors, get_stations
from aiogram.filters import BaseFilter
from aiogram.types import Message

class FilterNameDoctor(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        doctors = await get_doctors()
        for d in doctors:
            if message.text == d.name_doctor:
                return True
        else:
            return False

class FilterNameStation(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        stations = await get_stations()
        for st in stations:
            if st.name_station == message.text:
                return True
        else:
            return False
