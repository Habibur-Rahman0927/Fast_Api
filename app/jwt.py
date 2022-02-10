from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schema, database, models
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")




SECRET_KEY = "ASDF1234"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded


def verify_access_token(token: str, creadential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY)

        id: str = payload.get("users_id")

        if id is None:
            raise creadential_exception

        token_data = schema.TokenData(id = id)
    except JWTError:
        raise creadential_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    creadential_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authentication": "Bearer"})

    token = verify_access_token(token, creadential_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user