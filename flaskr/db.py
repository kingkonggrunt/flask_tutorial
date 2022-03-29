import sqlite3
from flask import Flask

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    """Grabs the database connection (if not already present) with dictionary parsing"""
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """Close the database connection (if present)"""
    db = g.pop('db', None)

    if db:
        db.close()

def init_db():
    """Initialize the database"""
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Wipes and Creates a new database"""
    init_db()
    click.echo('Initialized the Database')
    
def init_app(app: Flask):
    """
    App with close the db connection after responses
    App has the init-db cli command
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)