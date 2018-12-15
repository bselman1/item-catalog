from . import Base
from sqlalchemy.orm import mapper, relationship
from sqlalchemy import (
    ForeignKey,
    Table,
    Column,
    Integer,
    String
)


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

    category_items = relationship(
        'CategoryItem',
        back_populates='category',
        lazy='noload')

    def to_dict(self):
        item_dicts = []
        if self.category_items is not None:
            item_dicts = [item.to_dict() for item in self.category_items]
        category_dict = {
            'id': self.id,
            'name': self.name,
            'category_items': item_dicts
        }
        return {'category': category_dict}
