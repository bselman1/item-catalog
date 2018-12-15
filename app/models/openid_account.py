from . import Base
from sqlalchemy.orm import mapper, relationship
from sqlalchemy import ForeignKey, MetaData, Table, Column, Integer, String, Index

class OpenIdAccount(Base):
    __tablename__ = 'openid_account'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable = False)
    issuer_identifier = Column(String(255), nullable = False, index = True)
    subject_identifier = Column(String(255), nullable = False)

    user = relationship('User', back_populates='openid_accounts', lazy='noload')

    __table_args__ = (Index('open_id_account_iss_sub_ix', 'issuer_identifier', 'subject_identifier'),)