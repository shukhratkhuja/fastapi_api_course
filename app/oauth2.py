from jose import JWSError, jwt
from datetime import datetime, timedelta

# SECRET_KEY
# Algorithm
# Expiration time

SECRET_KEY = 'jh4g1kjh1j4hct242t4uy1t4u1vt4jk1g41tg4uy1tiu1t41cfgdhcgg34l1g546g367h537hbh'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})


    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

    return encoded_jwt

