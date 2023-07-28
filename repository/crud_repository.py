from abc import ABC, abstractmethod
from pydantic import BaseModel
from uuid import UUID
from db.session import DBSession


class CRUDRepository(ABC):
    @staticmethod
    @abstractmethod
    def create(obj: BaseModel, session: DBSession) -> BaseModel | None:
        ...

    @staticmethod
    @abstractmethod
    def read_all(session: DBSession) -> list[BaseModel]:
        ...

    @staticmethod
    @abstractmethod
    def read(id: UUID, session: DBSession) -> BaseModel | None:
        ...

    @staticmethod
    @abstractmethod
    def update(obj: BaseModel, session: DBSession) -> BaseModel | None:
        ...

    @staticmethod
    @abstractmethod
    def delete(id: UUID, session: DBSession) -> BaseModel | None:
        ...
