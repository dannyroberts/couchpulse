from sqlalchemy import Column, String, create_engine, Integer, Float, DateTime
from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from couchpulse import settings


engine = create_engine(settings.SQLALCHEMY_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class RequestLog(Base):
    __tablename__ = 'requests'
    id = Column(String, primary_key=True)
    method = Column(String)
    path = Column(String)
    params = Column(HSTORE)
    size = Column(Integer)
    time = Column(Float)
    timestamp = Column(DateTime, index=True)


class ResponseLog(Base):
    __tablename__ = 'responses'
    id = Column(String, primary_key=True)
    size = Column(Integer)
    time = Column(Float)
