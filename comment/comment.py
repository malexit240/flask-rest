from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from flaskr.auth.auth import login_required
from flaskr.db import get_db
from flaskr.comment.queries import (
    create_comment, delete_comment, get_comment, update_comment, comment_list # ============
)

bp = Blueprint("comment", __name__)

@bp.route('/create/<post_id>/<body>/', methods=("POST",))
def create(post_id,body):
    create_comment(get_db(),body,"",post_id)