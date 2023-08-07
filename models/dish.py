import uuid
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import BaseModel


class Dish(BaseModel):
    __tablename__ = 'dish'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    submenu_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('submenu.id', ondelete='CASCADE')
    )
    submenu: Mapped['Submenu'] = relationship(
        'Submenu', back_populates='dishes'
    )
