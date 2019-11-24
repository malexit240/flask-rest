"""this module contains routing functions for blog app"""

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify
from flask import Response
from werkzeug.exceptions import abort

from flaskr.auth.basic_auth import auth
from flaskr.db import get_db
from flaskr.blog.queries import (
    create_post, delete_post, get_post, update_post, get_post_list
)
from flaskr.auth.queries import get_user_by_id, get_user_by_username
from flaskr.comment.queries import get_comment_list

bp = Blueprint("blog", __name__,url_prefix="/blog")

@bp.route("/all/")
def index():
    """returns all the posts in json, most recent first."""
    db = get_db()
    posts = get_post_list(db)

    result = [{
            'id':p['id'],
            'title':p['title'],
            'body':p['body'],
            'created':p['created'],
            'author':p['username'],
            'comments':[{
                    'id':c['id'],
                    'body':c['body'],
                    'author':c['username'],
                    'created':c['created']
                }
                for c in get_comment_list(db,p['id'])
                ]
        } 
    for p in posts]

    return jsonify(result)


def check_post(id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    db = get_db()

    post = get_post(db, id)
    if not post:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author:
        if get_user_by_id(db,post['author_id']) != get_user_by_username(db,auth.username()):
            abort(403)

    return post


@bp.route("/create/", methods=("POST",))
@auth.login_required
def create():
    """Create a new post"""
    if request.method == "POST":
        error = None

        json = request.get_json()
        title = json['title']
        body = json['body']

        if not title:
            error = 'Title must be'
        elif not body:
            error +='Body must be'

        if not error:
            db = get_db()

            create_post(db, title, body, get_user_by_username(db,auth.username())['id'])
            return Response("post was added", status=200)
        else:
            flash(error)
            return Response('%s'%error,status=400)
            


    return Response("need POST method",status=405)


@bp.route("/update/<int:id>/", methods=("POST",))
@auth.login_required
def update(id):
    """Update a post if the current user is the author."""
    post = check_post(id)

    if not post:
        return Response("post not found",status=404)

    if request.method == "POST":
        error = None

        json = request.get_json()
        title = json['title']
        body = json['body']

        if not title:
            error = 'Title must be'
        elif not body:
            error +='Body must be'

        if not error:
            db = get_db()
            update_post(db, title, body, id)
            return Response('Post was updated',status=200)
        else:
            flash(error)
            return Response('%s'%error,status=400)

    return Response("need POST method",status=405)


@bp.route("/delete/<int:id>/", methods=("POST",))
@auth.login_required
def delete(id):
    """Delete a post.
    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    post = check_post(id)

    if not post:
        return Response("post not found",status=404)

    db = get_db()
    delete_post(db, id)

    return Response("post was deleted",status=200)
