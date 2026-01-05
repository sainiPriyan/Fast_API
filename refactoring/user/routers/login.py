from fastapi import APIRouter, Depends, status, Response, HTTPException
from .. import schemas, models, hashing
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    tags= ['Signin']
    
)


@router.post('/signup', response_model= schemas.ShowLoginDetails, )
def create_signup(request : schemas.LoginDetails, db: Session = Depends(get_db)):
    
    if db.query(models.LoginDetails).filter(models.LoginDetails.email == request.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email Id already exists')

    model = models.LoginDetails(name = request.name, password = hashing.bcrypt(request.password), email = request.email)
    db.add(model)
    db.commit()
    db.refresh(model)

    return model

@router.get('/getlogindetails/{id}', response_model= schemas.ShowLoginDetails)
def get_login_details(id:int, db:Session=Depends(get_db), response:Response=None):
    
    login = db.query(models.LoginDetails).filter(models.LoginDetails.id == id).first()
    
    if login is not None:
        return login
    
    else:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'Error':f"User with {id} NOT FOUND"}

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Login Details with id = {id} was NOT found") 