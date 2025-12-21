from fastapi import FastAPI, status, Response, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends


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

@app.post("/user/", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.User, db: Session = Depends(get_db)):

    if db.query(models.User).filter(models.User.phone == user.phone).first():
        return {"Error": "User with this phone number already exists."}

    new_user = models.User(name = user.name, age = user.age, phone = user.phone)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get('/user/all')

def get_all_users(db:Session=Depends(get_db)):
    return db.query(models.User).all()


@app.get('/user/{id}', status_code=status.HTTP_200_OK)

def get_use(id:int, db:Session=Depends(get_db), response:Response=None):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if user:
        return user
    
    else:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'Error':f"User with {id} NOT FOUND"}

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id = {id} was NOT found") 
    
@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)

def delete_user(id:int , db:Session=Depends(get_db), response:Response=None):
    
    user = db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)

    db.commit()

    return  {'details': f'user with id = {id} was deleted'}