from . import Base
from sqlalchemy.orm import mapper, relationship
from sqlalchemy import ForeignKey, MetaData, Table, Column, Integer, String


class CategoryItem(Base):
    __tablename__ = 'category_item'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    description = Column(String, nullable=True)

    category = relationship(
        'Category',
        back_populates='category_items',
        lazy='noload')

    def to_dict(self):
        item_dict = {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
        return {'category_item': item_dict}
