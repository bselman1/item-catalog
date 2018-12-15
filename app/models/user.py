from . import Base
from sqlalchemy.orm import mapper, relationship
from sqlalchemy import ForeignKey, MetaData, Table, Column, Integer, String


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=True)
    email = Column(String(255), nullable=True)

    openid_accounts = relationship(
        'OpenIdAccount',
        back_populates='user',
        lazy='noload')

    def is_active(self) -> bool:
        '''Assume all accounts are active'''
        return True

    def get_id(self) -> str:
        '''Returns the users unique identifier'''
        return str(self.id)

    def is_authenticated(self) -> bool:
        '''Assume all accounts are activated as they are built
        using OpenId providers'''
        return True

    def is_anonymous(self) -> bool:
        '''Always False as no anonymous users allowed'''
        return False
