"""
Application entry point.
"""

import os
import logging as lg

from core import create_app, db

from core.admin.models import Role, User

from dotenv import load_dotenv
from flask_migrate import Migrate
from core.contact.models import Contact
from core.main.models import Category, Project, Storie, Client


dotenv_path = os.path.join(os.path.dirname(__file__), '.flaskenv')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app(os.getenv('FLASK_CONFIG') or 'dev')
migrate = Migrate(app, db, render_as_batch=True)


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db, Role=Role,
        User=User, Category=Category,
        Project=Project, Client=Client,
        Contact=Contact, Storie=Storie
    )


@app.cli.command('init_db')
def init_db():
    db.create_all()
    Role.insert_roles()
    Category.insert_category()
    db.session.commit()
    lg.warning('Database initialized !')


if __name__ == "__main__":
    app.run(threaded=True)
