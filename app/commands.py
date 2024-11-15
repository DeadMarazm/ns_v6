from flask.cli import with_appcontext
import click
from flask_security import SQLAlchemyUserDatastore
from app import create_app, db
from app.models.models import User, Role

app = create_app()
user_datastore = SQLAlchemyUserDatastore(db, User, Role)  # Create datastore instance


@click.command(name='shell')
@with_appcontext
def shell():
    import code
    shell_context = dict(db=db, app=app, User=User, Role=Role)
    code.interact(local=shell_context)


app.cli.add_command(shell)
