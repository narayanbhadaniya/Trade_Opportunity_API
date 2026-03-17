from jose import jwt

SECRET = "secret"

def create_token(username):
    return jwt.encode({"user": username}, SECRET, algorithm="HS256")

def verify_token(token):
    return jwt.decode(token, SECRET, algorithms=["HS256"])
