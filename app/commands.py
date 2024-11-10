from flask.cli import with_appcontext
import click
from flask_security import SQLAlchemyUserDatastore
from app import create_app, db, security
from app.models.models import User, Role

app = create_app()
user_datastore = SQLAlchemyUserDatastore(db, User, Role) # Create datastore instance

@click.command(name='shell')
@with_appcontext
def shell():
    shell_context = dict(db=db, app=app, user_datastore=security.datastore)
    return shell_context

if __name__ == '__main__':
    app.cli.add_command(shell)
