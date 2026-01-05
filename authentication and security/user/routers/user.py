from fastapi import APIRouter, Depends, status, Response, HTTPException
from .. import schemas, models, oauth2
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db
from ..repository import user


router = APIRouter(
    tags= ['User'],
    prefix= '/user'
)


@router.get('/all', response_model=List[schemas.ShowUser])
def get_all_users(db:Session=Depends(get_db), current_user: schemas.Login = Depends(oauth2.get_current_user)):
    return user.get_all(db)


@router.get("/")
def read_root( current_user: schemas.Login = Depends(oauth2.get_current_user)):
    return {"Hello": "World"}

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user_scehma: schemas.User, db: Session = Depends(get_db), current_user: schemas.Login = Depends(oauth2.get_current_user)):
    return user.create(user_scehma,db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_user(id:int, db:Session=Depends(get_db), response:Response=None, current_user: schemas.Login = Depends(oauth2.get_current_user)):
   return user.get(id,db)
    
    
@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id:int , db:Session=Depends(get_db), response:Response=None, current_user: schemas.Login = Depends(oauth2.get_current_user)):
    return user.delete(id,db)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request:schemas.User, db: Session = Depends(get_db),  current_user: schemas.Login = Depends(oauth2.get_current_user)):
    user.update(id,request,db)