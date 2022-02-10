from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import database, schema, models, utils, jwt

router = APIRouter(tags=['Authentication'])

@router.post('/login',response_model = schema.Token)
def login(user_credentials: schema.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invaild Creadentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invaild Creadentials")

    access_token = jwt.create_access_token(data = {"users_id": user.id})

    return {"access_token" : access_token, "token_type": "bearer"}
