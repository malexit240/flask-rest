"""this module contains function for queries to db"""

from werkzeug.security import generate_password_hash


def get_user_by_id(db, id):
    """returns a user from db by id"""
    return db.execute(
        "SELECT * FROM user WHERE id = ?", (id,)
    ).fetchone()


def get_user_by_username(db, username):
    """returns a user from db by username"""
    return db.execute(
        "SELECT * FROM user WHERE username = ?", (username,)
    ).fetchone()


def create_user(db, username, password):
    """create a user in db
    
    username--username of user
    password--'raw' password without hashing
    """
    db.execute(
        "INSERT INTO user(username,password) VALUES(?,?)",
        (username, generate_password_hash(password)),
    )
    db.commit()
