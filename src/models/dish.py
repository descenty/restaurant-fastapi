from decimal import Decimal
import uuid
from sqlalchemy import ForeignKey, String, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column, Mapped
from models.base import Base
from models.submenu import Submenu


class Dish(Base):
    __tablename__ = "dish"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    desсription: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    submenu_id: Mapped[UUID] = mapped_column(ForeignKey("submenu.id"))
    submenu: Mapped[Submenu] = relationship(back_populates="dishes")
