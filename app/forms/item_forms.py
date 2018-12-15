from typing import Sequence
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, FormField
from wtforms.validators import DataRequired, Length
from app.models import CategoryItem, Category

class ItemForm(FlaskForm):
    name = StringField('Name', id='item_name', validators=[DataRequired(), Length(min=1, max=100)])
    description = StringField('Description', id='item_description', validators=[DataRequired()])
    category = SelectField('Category', id='item_category', coerce=int, validators=[DataRequired()])
        
    def set_categories(self, categories: Sequence[Category]):
        self.category.choices = [(c.id, c.name) for c in categories]

    def build_item(self):
        item = CategoryItem()
        item.name = self.name.data
        item.description = self.description.data
        item.category_id = self.category.data
        return item

class NewItemForm(ItemForm):
    submit = SubmitField('Create')

class EditItemForm(ItemForm):
    submit = SubmitField('Update')

    def set_item(self, category_item: CategoryItem, categories: Sequence[Category]):
        self.set_categories(categories)
        self.category_item = category_item
        self.name.data = category_item.name
        self.category.data = category_item.category_id
        self.description.data = category_item.description
