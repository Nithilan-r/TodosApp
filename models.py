from database import Base
# creating model for databse.py file
from sqlalchemy import Column,Integer,String,Boolean

class Todos(Base):
    __tablename__='todos'
    #will let SQlchemy to name table inside database

    id=Column(Integer,primary_key=True,index=True)
    #id going to be primery key or primery idetifier unique for each item
    #index signifies indexable that going to be unique

    title=Column(String)
    description=Column(String)
    priority=Column(Integer)
    complete=Column(Boolean)