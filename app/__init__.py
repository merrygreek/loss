import logging
import os

from flask import Flask
from flask_appbuilder import AppBuilder, SQLA

from flask_dropzone import Dropzone

"""
 Logging configuration
"""

basedir = os.path.abspath(os.path.dirname(__file__))


logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)

app.config.from_object("config")
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = '.xls, .xlsx'

app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'static/uploads'),
    # Flask-Dropzone config:
    DROPZONE_MAX_FILE_SIZE=10,
    DROPZONE_MAX_FILES=30,
    DROPZONE_DEFAULT_MESSAGE='点击空白处,或者把文件拖到这里上传,支持多选',
    DROPZONE_PARALLEL_UPLOADS=3,  # set parallel amount
    DROPZONE_UPLOAD_MULTIPLE=True,  # enable upload multiple
)

dropzone = Dropzone(app)

db = SQLA(app)
appbuilder = AppBuilder(app, db.session)


"""
from sqlalchemy.engine import Engine
from sqlalchemy import event

#Only include this for SQLLite constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Will force sqllite contraint foreign keys
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
"""

from . import views
