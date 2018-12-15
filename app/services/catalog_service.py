from typing import Sequence, Tuple
from sqlalchemy.orm import sessionmaker, contains_eager
from app.models import Category, CategoryItem, DbSetup
from app.forms import NewItemForm, EditItemForm

class CatalogService:
    def __init__(self, dbsetup: DbSetup):
        self.dbsetup = dbsetup

    def get_catalog(self) -> Sequence[Category]:
        """Returns the full catalog of Category objects with their category_items property loaded."""
        session = self.dbsetup.create_session()
        categories = session.query(Category) \
                            .outerjoin(CategoryItem) \
                            .options(contains_eager(Category.category_items)) \
                            .all()
        session.close()
        return categories

    def get_categories(self) -> Sequence[Category]:
        """Returns Category objects without their category_items loaded."""
        session = self.dbsetup.create_session()
        categories =  session.query(Category) \
                             .order_by(Category.name) \
                             .all()
        session.close()
        return categories
    
    def get_category(self, category_name: str) -> Category:
        """Returns a Category object loaded with its child items"""
        session = self.dbsetup.create_session()
        category = session.query(Category) \
                          .outerjoin(CategoryItem) \
                          .filter(Category.name == category_name) \
                          .options(contains_eager(Category.category_items)) \
                          .one_or_none()
        session.close()
        return category

    def get_category_item(self, category_item_id: int) -> CategoryItem:
        """Returns a CategoryItem object associated with the provided id if it exists, else None"""
        session = self.dbsetup.create_session()
        item = session.query(CategoryItem) \
                      .filter(CategoryItem.id == category_item_id) \
                      .one_or_none()
        session.close()
        return item

    def delete_category_item(self, category_item_id: int) -> CategoryItem:
        """Deletes a category item if it exists"""
        session = self.dbsetup.create_session()
        item = session.query(CategoryItem) \
                      .filter(CategoryItem.id == category_item_id) \
                      .one_or_none()
        if item is not None:
            session.delete(item)
            session.commit()
        session.close()
        return item

    def save_category_item(self, form: NewItemForm) -> CategoryItem:
        session = self.dbsetup.create_session()
        item = form.build_item()
        session.add(item)
        session.commit()
        session.close()
        return item

    def update_category_item(self, form: EditItemForm, item_id: int) -> CategoryItem:
        new_item = form.build_item()
        new_item.id = item_id

        #Get the old item from the database and update its values before committing changes.
        session = self.dbsetup.create_session()
        old_item = session.query(CategoryItem) \
                          .filter(CategoryItem.id == item_id) \
                          .one()
        old_item.name = new_item.name
        old_item.description = new_item.description
        old_item.category_id = new_item.category_id
        session.commit()
        session.close()
        return new_item