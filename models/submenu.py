import uuid
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID
from models.base import BaseModel


class Submenu(BaseModel):
    __tablename__ = "submenu"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    menu_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("menu.id", ondelete="CASCADE")
    )
    menu: Mapped["Menu"] = relationship("Menu", back_populates="submenus")
    dishes: Mapped[list["Dish"]] = relationship(
        "Dish", back_populates="submenu", cascade="all, delete-orphan"
    )
