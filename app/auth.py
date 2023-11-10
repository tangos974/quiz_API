from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

# Id and password dictionary 
users_credentials = {
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine"
}

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    user = credentials.username
    password = credentials.password

    if user not in users_credentials or users_credentials[user] != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    return user