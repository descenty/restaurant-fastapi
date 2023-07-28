import uuid
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column, Mapped
from models.base import BaseModel


class Menu(BaseModel):
    __tablename__ = "menu"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    submenus: Mapped[list["Submenu"]] = relationship(
        "Submenu", back_populates="menu", cascade="all, delete-orphan"
    )
