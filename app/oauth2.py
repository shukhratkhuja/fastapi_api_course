from jose import JWSError, jwt
from datetime import datetime, timedelta
import datetime as dt
from . import schemas
from fastapi import Depends, status, HTTPException

from fastapi.security import OAuth2PasswordBearer

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')


# SECRET_KEY
# Algorithm
# Expiration time

SECRET_KEY = 'jh4g1kjh1j4hct242t4uy1t4u1vt4jk1g41tg4uy1tiu1t41cfgdhcgg34l1g546g367h537hbh'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(dt.timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})


    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = [ALGORITHM])

    return encoded_jwt



def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)

        id = payload.get("user_id")

        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id)
    
    except JWSError:

        raise credentials_exception

    return token_data
    

def get_current_user(token: str = Depends(oauth2_schema)):

    credentials_exception = HTTPException(
                                        status_code=status.HTTP_401_UNAUTHORIZED, 
                                        detail=f"Could not validate credentials", 
                                        headers={"WWW-Authenticate": "Bearer"})
    
    return verify_access_token(token=token, credentials_exception=credentials_exception)
