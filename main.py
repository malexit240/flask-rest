import os

from flask import Flask


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    app.config.from_pyfile('config.py', silent=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the database commands
    from flaskr import db

    db.init_app(app)

    # apply the blueprints to the app
    from flaskr.blog import blog
    from flaskr.auth import auth
    from flaskr.comment import comment

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(comment.bp)

    return app
