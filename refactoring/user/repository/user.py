from sqlalchemy.orm import Session
from .. import schemas, models
from fastapi import status, HTTPException

def get_all(db:Session):
    return db.query(models.User).all()

def create(user: schemas.User, db: Session):
    if db.query(models.User).filter(models.User.phone == user.phone).first():
        return {"Error": "User with this phone number already exists."}

    new_user = models.User(name = user.name, age = user.age, phone = user.phone, login_id =1 )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def get(id:int, db:Session):

    u = db.query(models.User).filter(models.User.id == id).first()
    
    if u is not None:
        return u
    else:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'Error':f"User with {id} NOT FOUND"}

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id = {id} was NOT found") 

def delete(id:int , db:Session):
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id = {id} was NOT found")
    
    user.delete(synchronize_session=False)
    db.commit()
    return  {'details': f'user with id = {id} was deleted'}

def update(id: int, request:schemas.User, db: Session):
    
    user  = db.query(models.User).filter(models.User.id == id)
    
    if user.first():
        user.name = request.name
        user.age = request.age
        user.phone = request.phone
        db.commit()
        return {'deatials': 'User details updates'}
    
    db.add(models.User(id=id, name=request.name, age=request.age, phone=request.phone))
    db.commit()

    return {'detail':'New user created'}