# -*- coding: utf-8 -*-
"""Create an application instance."""
from flask.helpers import get_debug_flag
from recipeapp.app import app_factory
from recipeapp.config import DevConfig, ProdConfig

CONFIG = DevConfig if get_debug_flag() else ProdConfig

application = app_factory(CONFIG)
