from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.event import listen

Base = declarative_base()

from .category import Category  # noqa: E402
from .category_item import CategoryItem  # noqa: E402
from .user import User  # noqa: E402
from .openid_account import OpenIdAccount  # noqa: E402
from .db_setup import DbSetup  # noqa: E402


def init_app(app):
    pass
