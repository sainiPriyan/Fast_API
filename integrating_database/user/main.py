from fastapi import FastAPI, status, Response, HTTPException
from . import schemas, models, hashing
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List



app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()    


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/user/", status_code=status.HTTP_201_CREATED, tags= ['User'])
def create_user(user: schemas.User, db: Session = Depends(get_db)):

    if db.query(models.User).filter(models.User.phone == user.phone).first():
        return {"Error": "User with this phone number already exists."}

    new_user = models.User(name = user.name, age = user.age, phone = user.phone, login_id =1 )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get('/user/all', response_model=List[schemas.ShowUser], tags= ['User'])
def get_all_users(db:Session=Depends(get_db)):
    return db.query(models.User).all()


@app.get('/user/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser, tags= ['User'])
def get_user(id:int, db:Session=Depends(get_db), response:Response=None):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if user is not None:
        return user
    
    else:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'Error':f"User with {id} NOT FOUND"}

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id = {id} was NOT found") 
    
@app.delete('/user/{id}',status_code=status.HTTP_204_NO_CONTENT, tags= ['User'])

def delete_user(id:int , db:Session=Depends(get_db), response:Response=None):
    
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id = {id} was NOT found")


    user.delete(synchronize_session=False)

    db.commit()

    return  {'details': f'user with id = {id} was deleted'}

@app.put('/user/{id}', status_code=status.HTTP_202_ACCEPTED, tags= ['User'])
def update(id: int, request:schemas.User, db: Session = Depends(get_db)):
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

@app.post('/signup', response_model= schemas.ShowLoginDetails, tags= ['Signin'])
def create_signup(request : schemas.LoginDetails, db: Session = Depends(get_db)):
    
    if db.query(models.LoginDetails).filter(models.LoginDetails.email == request.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email Id already exists')

    model = models.LoginDetails(name = request.name, password = hashing.bcrypt(request.password), email = request.email)
    db.add(model)
    db.commit()
    db.refresh(model)

    return model

@app.get('/getlogindetails/{id}', response_model= schemas.ShowLoginDetails, tags= ['Signin'])
def get_login_details(id:int, db:Session=Depends(get_db), response:Response=None):
    
    login = db.query(models.LoginDetails).filter(models.LoginDetails.id == id).first()
    
    if login is not None:
        return login
    
    else:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'Error':f"User with {id} NOT FOUND"}

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Login Details with id = {id} was NOT found") 