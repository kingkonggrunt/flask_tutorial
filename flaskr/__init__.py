import os

from flask import Flask


def create_app(test_config=None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite")
    )
    
    # load the test_config if given, else load the instance config
    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_pyfile('config.py', silent=True)

    # create the instance folder (if not already present)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # hello world route
    @app.route("/hello")
    def hello():
        return "Hello World!"

    from . import db
    db.init_app(app)
    
    from . import auth
    from . import blog
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint='index')
    
    return app