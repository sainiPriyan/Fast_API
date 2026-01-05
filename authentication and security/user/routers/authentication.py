from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from.. import schemas, database, models, hashing, JWT
from sqlalchemy.orm import Session

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(database.get_db)):
    user = db.query(models.LoginDetails).filter(models.LoginDetails.email == request.username).first()
    
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f'Invalid credentials')

    if not  hashing.verify(request.password,user.password):
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f'Invalid credentials(password)')

    access_token = JWT.create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type':'bearer'}
