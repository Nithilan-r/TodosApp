from pydantic import BaseModel ,Field
from typing_extensions import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI,Depends,HTTPException,Path
from starlette import status
import models
from models import Todos
from database import engine

app=FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()
    #contact database
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]

class TodoRequest(BaseModel):
    title:str=Field(min_length=3)
    description:str=Field(min_length=3,max_length=100)
    priority:str=Field(gt=0,lt=6)
    complete:bool

@app.get("/")
async def read_all(db:db_dependency):
    return db.query(Todos).all()
#depends is dependency injection,means to do something before we exexute if we want to execute

@app.get("/todo/{todo_id}",status_code=status.HTTP_200_OK)
async def read_todo(db:db_dependency,todo_id:int=Path(gt=0)):
    todo_model=db.query().filter(Todos.id==todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404,detail='Todo not found')

@app.post("/todo",status_code=status.HTTP_201_CREATED)
async def create_todo(db:db_dependency,todo_request:TodoRequest):
    todo_model=Todos(**todo_request.dict())

    db.add(todo_model)
    db.commit()

#TodoRequest has to be above path parameters
@app.put("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db:db_dependency,todo_request:TodoRequest,todo_id:int=Path(gt=0),):
    todo_model=db.query(Todos).filter(Todos.id==todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail='Todo not found')
    todo_model.title=todo_request.title
    todo_model.description=todo_request.description
    todo_model.priority=todo_request.priority
    todo_model.complete=todo_request.complete

    db.add(todo_model)
    db.commit()

@app.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()

    db.commit()