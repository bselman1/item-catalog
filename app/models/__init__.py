from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.event import listen

Base = declarative_base()

from .category import Category
from .category_item import CategoryItem
from .user import User
from .openid_account import OpenIdAccount
from .db_setup import DbSetup

def init_app(app):
    pass