"""this module contains global constants 'auth' for basic authorization on system"""

from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from flaskr.db import get_db
from flaskr.auth.queries import get_user_by_username



auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username,password):
    """returns True if username and password is valid"""
    
    db = get_db()
    user = get_user_by_username(db,username)
    if user:
        return check_password_hash(user['password'],password)
    else:
        return False