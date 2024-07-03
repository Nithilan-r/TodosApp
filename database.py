from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL='sqlite:///./todos.db'
#used to create location of database on fastapi application

#create engine of database. engine used to open up connection or use datbase
engine=create_engine(SQLALCHEMY_DATABASE_URL,connect_args={'check_same_thread':False})
#connect args used to define some kind of connection

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
#autocommit flush false so databse does not do anything on own to have full control

Base=declarative_base()