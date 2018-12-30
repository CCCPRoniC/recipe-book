# -*- coding: utf-8 -*-
from flask import Blueprint

recipe = Blueprint('recipes', __name__, url_prefix='/recipes/')
