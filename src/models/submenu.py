import uuid
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID
from models.base import Base
from models.dish import Dish
from models.menu import Menu


class Submenu(Base):
    __tablename__ = "submenu"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    desсription: Mapped[str] = mapped_column(String(255), nullable=False)
    menu_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("menu.id")
    )
    menu: Mapped[Menu] = relationship(Menu, back_populates="submenus")
    dishes: Mapped[list[Dish]] = relationship(
        back_populates="submenu", cascade="all, delete-orphan"
    )
