from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:////tmp/test.db",
        convert_unicode=True)
session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine))

Base = declarative_base()
Base.query = session.query_property()

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

class Feed(Base):
    __tablename__ = 'feeds'
    id = Column(Integer, primary_key=True)
    link = Column(String(150))
    keywords = relationship("Keyword")
    description = Column(String(200))
    favicon = Column(String(150))

    def rep(self):
        return({c.name: getattr(self, c.name) for c in self.__table__.columns})

    def __init__(self, link, keywords=(), description=None, favicon=None):
        #keywords is initialized when function is defined so
        self.link = link
        self.keywords = [Keyword(word) for word in keywords]
        self.description = description
        self.favicon = favicon

class Keyword(Base):
    __tablename__ = "keywords"
    id = Column(Integer, primary_key=True)
    word = Column(String(40))
    feed_id = Column(Integer, ForeignKey('feeds.id'))

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return("User({}, {})".format(self.name, self.email))

def init_db():
    #import all modules here that might define models
    # so that they will be registered properly on the
    # metadata. Otherwise you will have to import them
    # first before calling init_db()
    Base.metadata.create_all(bind=engine)
