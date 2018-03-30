from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c3209OIOPP901QOU8c2u'
socketio = SocketIO(app, message_queue='redis://localhost:6379')

# file_path = os.path.abspath(os.getcwd())+"\database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from .models import (
    Player, Question, Option, Weight, Faction, Schedule, Log, Answer,
    Avatar
)

admin = Admin(app, name='Faction Master', template_mode='bootstrap3',
              url='/admin123gh1g2hvh12gvh312us1jsc1j2sj12sf3t2f1stf3y123')
admin.add_view(ModelView(Player, db.session))
admin.add_view(ModelView(Question, db.session))
admin.add_views(
    ModelView(Option, db.session),
    ModelView(Weight, db.session),
    ModelView(Faction, db.session),
    ModelView(Schedule, db.session),
    ModelView(Log, db.session),
    ModelView(Answer, db.session),
    ModelView(Avatar, db.session),

)


from celery import Celery

def make_celery(app):
    celery = Celery(app.import_name,
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
)

celery = make_celery(app)
from app import schedule
from app import views