from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Article(Base):
    """Model for Articles"""
    __tablename__ = 'articles'

    _id = Column(Integer, primary_key=True)
    source = Column(String)
    title = Column(String)
    url = Column(String)
    author = Column(String)
    date_published = Column(DateTime)

    def __init__(self, article):
        self.source = article.source
        self.title = article.title
        self.url = article.url
        self.author = article.author
        self.date_published = article.date_published

    def __repr__(self):
        return ("<Article(source={0}, title={1}, url={2}, author={3}, "
                "date_published={4})>".format(self.source, self.title,
                self.url, self.author, self.date_published))

engine = create_engine('')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
db_session = DBSession()
