from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import hashlib

mysql_db = create_engine('mysql://mathew:p455w0rd@localhost/hero_fish_db', echo=True)

Base = declarative_base()

class User(Base):

    __tablename__ = 'users'
    id       = Column(Integer(11), primary_key=True)
    name     = Column(String(50))
    fullname = Column(String(125))
    password = Column(String(64))

    def __init__(self, name, fullname, password):
        self.name     = name
        self.fullname = fullname
        self.password = hashlib.sha1(password).hexdigest()

    def __repr__(self):
        return "<User('%s', '%s', '%s')>" % (self.name, self.fullname, self.password)

metadata = Base.metadata
metadata.create_all(mysql_db)

Session = sessionmaker(bind=mysql_db)
session = Session()
