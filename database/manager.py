from typing import Sequence, Self

from sqlalchemy import select, update as sqlalchemy_update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload, load_only

from .connection import db


class Manager:
    class DoesNotExists(Exception):
        pass

    @classmethod
    async def get(cls, select_in_load: str | None = None, **kwargs) -> Self:
        """
        # Возвращает одну запись, которая удовлетворяет введенным параметрам.

        :param select_in_load: Загрузить сразу связанную модель.
        :param kwargs: Поля и значения.
        :return: Объект или вызовет исключение DoesNotExists.
        """

        params = [getattr(cls, key) == val for key, val in kwargs.items()]
        query = select(cls).where(*params)

        if select_in_load:
            query.options(selectinload(getattr(cls, select_in_load)))

        try:
            async with db.session() as session:
                results = await session.execute(query)
                (result,) = results.one()
                return result
        except NoResultFound:
            raise cls.DoesNotExists

    @classmethod
    async def create(cls, **kwargs) -> Self:
        obj = cls(**kwargs)
        async with db.session() as session:
            session.add(obj)
            await session.commit()
            await session.refresh(obj)  # Получить ID созданного объекта
        return obj

    async def update(self, **kwargs) -> None:
        """
        # Обновляет текущий объект.
        :param kwargs: Поля и значения, которые надо поменять.
        """

        async with db.session() as session:
            await session.execute(
                sqlalchemy_update(self.__class__), [{"id": self.id, **kwargs}]
            )
            await session.commit()

    @classmethod
    async def all(
        cls, select_in_load: str = None, values: list[str] = None
    ) -> Sequence[Self]:
        """
        # Получает все записи.

        :param select_in_load: Загрузить сразу связанную модель.
        :param values: Список полей, которые надо вернуть, если нет, то все (default None).
        """

        if values and isinstance(values, list):
            # Определенные поля
            values = [getattr(cls, val) for val in values if isinstance(val, str)]
            query = select(cls).options(load_only(*values))
        else:
            # Все поля
            query = select(cls)

        if select_in_load:
            query.options(selectinload(getattr(cls, select_in_load)))

        async with db.session() as session:
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def filter(
        cls, select_in_load: str | None = None, **kwargs
    ) -> Sequence[Self]:
        """
        # Возвращает все записи, которые удовлетворяют фильтру.

        :param select_in_load: Загрузить сразу связанную модель.
        :param kwargs: Поля и значения.
        :return: Перечень записей.
        """

        params = [getattr(cls, key) == val for key, val in kwargs.items()]
        query = select(cls).where(*params)

        if select_in_load:
            query.options(selectinload(getattr(cls, select_in_load)))

        try:
            async with db.session() as session:
                results = await session.execute(query)
                return results.scalars().all()
        except NoResultFound:
            return ()
