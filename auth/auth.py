"""this module contains routing function for register new user"""

import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import Response



from flaskr.db import get_db
from flaskr.auth.queries import (
    create_user, get_user_by_id, get_user_by_username
)


bp = Blueprint("auth", __name__, url_prefix="/auth") # union of views

@bp.route("/register/", methods=("POST",))
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """

    if request.method == "POST":
        db = get_db()
        error = None

        json = request.get_json()
        username = json['username']
        password = json['password']

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif get_user_by_username(db, username) is not None:
            error = "User {0} is already registered.".format(username)

        if not error:
            create_user(db, username, password)
            return Response("200 user was created",status=200)

        return Response("400 %s"%error,status=400)

    return Response("405 need POST method",status=405)

    