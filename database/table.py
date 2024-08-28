from sqlalchemy import BigInteger, ForeignKey, String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url="sqlite+aiosqlite:///database/db.sqlite3", echo=False)
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Stations(Base):
    __tablename__ = 'station'
    name_station: Mapped[str] = mapped_column(primary_key=True)
    phone: Mapped[str] = mapped_column(String)
    adress: Mapped[str] = mapped_column(String)
    link_lokation: Mapped[str] = mapped_column(String)

class Doctors(Base):
    __tablename__ = 'doctors'
    name_doctor: Mapped[str] = mapped_column(primary_key=True)
    adress_doctor: Mapped[str] = mapped_column(String)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)