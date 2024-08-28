from database.table import Stations, Doctors
from database.table import async_session
from sqlalchemy import select
from dataclasses import dataclass


@dataclass
class UserRole:
    user ='user'
    admin = 'admin'

async def add_station(data: dict):
    async with async_session() as session:
        station = await session.scalar(select(Stations).where(Stations.name_station == data['name_station']))
        if not station:
            session.add(Stations(**data))
            await session.commit()

async def get_stations() -> Stations:
    async with async_session() as session:
        return await session.scalars(select(Stations))

async def get_anythink_station(name_station: str) -> Stations:
    async with async_session() as session:
        return await session.scalar(select(Stations).where(Stations.name_station == name_station))



async def add_doctor(data: dict):
    async with async_session() as session:
        doctor = await session.scalar(select(Doctors).where(Doctors.name_doctor == data['name_doctor']))
        if not doctor:
            session.add(Doctors(**data))
            await session.commit()

async def get_doctors() -> Doctors:
    async with async_session() as session:
        return await session.scalars(select(Doctors))

async def get_adress_doctor(name_doctor: str) -> Doctors:
    async with async_session() as session:
        return await session.scalar(select(Doctors).where(Doctors.name_doctor == name_doctor))

async def del_doctor(name_doctor):
    async with async_session() as session:
        doctor = await session.scalar(select(Doctors).where(Doctors.name_doctor == name_doctor))
        if doctor:
            session.delete(doctor)
            await session.commit()
