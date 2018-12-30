# -*- coding: utf-8 -*-
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension
from flask_navbar import Nav
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()
debug_toolbar = DebugToolbarExtension()
bootstrap = Bootstrap()
nav = Nav()
security = Security()
