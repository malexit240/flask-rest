"""this module contains routing function for comment app"""

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import Response
from werkzeug.exceptions import abort

from flaskr.auth.basic_auth import auth
from flaskr.db import get_db
from flaskr.auth.queries import get_user_by_username, get_user_by_id
from flaskr.comment.queries import (
    create_comment, delete_comment, get_comment, update_comment
)

bp = Blueprint("comment", __name__,url_prefix='/comment')

def check_attrs_in_json(jsonlike:dict,*args):
    """returns True if dict contains keys from args"""
    if not len(args):
        return False
    
    for attr in args:
        if attr not in jsonlike:
            return False

    return True

def check_comment(id, check_author=True):
    """Get a comment and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.
    """

    db = get_db()

    comment = get_comment(db, id)
    if not comment:
        abort(404, "Comment id {0} doesn't exist.".format(id))

    if check_author:
        if get_user_by_username(db,comment['username']) != get_user_by_username(db,auth.username()):
            abort(403)

    return comment

@bp.route("/create/<int:post_id>/", methods=("POST",))
@auth.login_required
def create(post_id:int):
    """Create a new comment for the current user."""
    if request.method == "POST":


        json = request.get_json()
        body = json['body']
        author_id =get_user_by_username(get_db(),auth.username())['id']

        if check_attrs_in_json(json,'body'):
            create_comment(get_db(),body,author_id,post_id)
            return Response("comment was added", status=200)
        else:
            error = 'incorrect json'
            flash(error)
            return Response('%s'%error,status=400)

    return Response("need POST method",status=405)


@bp.route("/update/<int:id>/", methods=("POST",))
@auth.login_required
def update(id):
    """Update a comment if the current user is the author"""
    comment = check_comment(id)

    if not comment:
        return Response("comment not found",status=404)

    if request.method == "POST":
        error = None

        json = request.get_json()
        body = json['body']

        if check_attrs_in_json(json,'body'):
            db = get_db()
            update_comment(db, body, id)
            return Response('comment was updated',status=200)
        else:
            error = 'incorrect json'
            flash(error)
            return Response('%s'%error,status=400)

    return Response("need POST method",status=405)


@bp.route("/delete/<int:id>/", methods=("POST",))
@auth.login_required
def delete(id):
    """Delete a comment"""
    
    comment = check_comment(id)

    if not comment:
        return Response("comment not found",status=404)

    db = get_db()
    delete_comment(db, id)

    return Response("comment was deleted",status=200)
