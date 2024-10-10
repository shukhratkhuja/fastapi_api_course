from jose import JWSError, exceptions, jwt
from datetime import datetime, timedelta
import datetime as dt
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from .config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(dt.timezone.utc) + timedelta(minutes=settings.access_token_expire_time)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm = settings.algorithm)
 
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token=token, key=settings.secret_key, algorithms=[settings.algorithm])
        id = payload.get("user_id")

        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id)
    
    except exceptions.ExpiredSignatureError:
    
        raise credentials_exception 
    
    except JWSError:

        raise credentials_exception

    return token_data
    

def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(database.get_db)):

    credentials_exception = HTTPException(
                                        status_code=status.HTTP_401_UNAUTHORIZED, 
                                        detail=f"Could not validate credentials", 
                                        headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token=token, credentials_exception=credentials_exception)
    

    user = db.query(models.User).filter(models.User.id == token.id).first()

    # print("USER", user)
    
    return user
