from flask.cli import FlaskGroup
from sqlalchemy import inspect

from controller import app, db

cli = FlaskGroup(app)


@cli.command('create_db')
def create_db():
    inspector = inspect(db.engine)
    if not inspector.has_table('questions'):
        db.create_all()
        db.session.commit()


if __name__ == '__main__':
    cli()
