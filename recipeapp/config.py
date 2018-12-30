# -*- coding: utf-8 -*-
"""Application configuration."""
import logging
import os


class Config(object):
    """Base configuration."""
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, '..'))

    SECRET_KEY = 'BeefW3ll1ngton'
    BCRYPT_LOG_ROUNDS = 13
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_LEVEL = logging.DEBUG
    TEMPLATE_DIR = os.path.join(PROJECT_ROOT, 'templates')
    STATIC_DIR = os.path.join(TEMPLATE_DIR, 'static')


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    LOG_LEVEL = logging.WARN

    # RDS Configuration
    if 'RDS_HOSTNAME' in os.environ:
        DB_NAME = os.environ['RDS_DB_NAME']
        DB_USER = os.environ['RDS_USERNAME']
        DB_PASSWORD = os.environ['RDS_PASSWORD']
        DB_HOST = os.environ['RDS_HOSTNAME']
        DB_PORT = os.environ['RDS_PORT']
        SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{password}@{host}:{port}/{db}'.format(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            db=DB_NAME
        )


class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True
    # Put the db file in project root
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    DEBUG_TB_ENABLED = True


class TestConfig(Config):
    """Test configuration."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    BCRYPT_LOG_ROUNDS = 4  # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
    WTF_CSRF_ENABLED = False  # Allows form testing
    DEBUG_TB_ENABLED = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
