# -*- coding: utf-8 -*-
""" Click commands. Commands are taken from https://github.com/sloria/cookiecutter-flask. """
import os
import click
from glob import glob
from subprocess import call
from flask import current_app
from flask.cli import with_appcontext
from werkzeug.exceptions import MethodNotAllowed, NotFound
from extensions import db
from models import Role, User

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)


@click.command()
def clean():  # pragma: no cover
    """
    Remove *.pyc and *.pyo files recursively starting at current directory.
    Borrowed from Flask-Script, converted to use Click.
    """
    for dirpath, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            if filename.endswith('.pyc') or filename.endswith('.pyo'):
                full_pathname = os.path.join(dirpath, filename)
                click.echo('Removing {}'.format(full_pathname))
                os.remove(full_pathname)


@click.command()
@click.option('-f', '--fix-imports', default=False, is_flag=True, help='Fix imports using isort, before linting')
def lint(fix_imports):  # pragma: no cover
    """Lint and check code style with flake8 and isort."""
    skip = ['requirements', 'env', 'node_modules']
    root_files = glob('*.py')
    root_directories = [
        name for name in next(os.walk('.'))[1] if not name.startswith('.')]
    files_and_directories = [
        arg for arg in root_files + root_directories if arg not in skip]

    def execute_tool(description, *args):
        """Execute a checking tool with its arguments."""
        command_line = list(args) + files_and_directories
        click.echo('{}: {}'.format(description, ' '.join(command_line)))
        rv = call(command_line)
        if rv != 0:
            exit(rv)

    if fix_imports:
        execute_tool('Fixing import order', 'isort', '-rc')
    execute_tool('Checking code style', 'flake8')


@click.command()
@click.option('--url', default=None, help='Url to test (ex. /static/image.png)')
@click.option('--order', default='rule', help='Property on Rule to order by (default: rule)')
@with_appcontext
def urls(url, order):  # pragma: no cover
    """
    Display all of the url matching routes for the project.
    Borrowed from Flask-Script, converted to use Click.
    """
    rows = []
    column_headers = ('Rule', 'Endpoint', 'Arguments')

    if url:
        try:
            rule, arguments = (
                current_app.url_map
                           .bind('localhost')
                           .match(url, return_rule=True))
            rows.append((rule.rule, rule.endpoint, arguments))
            column_length = 3
        except (NotFound, MethodNotAllowed) as e:
            rows.append(('<{}>'.format(e), None, None))
            column_length = 1
    else:
        rules = sorted(
            current_app.url_map.iter_rules(),
            key=lambda rule: getattr(rule, order))
        for rule in rules:
            rows.append((rule.rule, rule.endpoint, None))
        column_length = 2

    str_template = ''
    table_width = 0

    if column_length >= 1:
        max_rule_length = max(len(r[0]) for r in rows)
        max_rule_length = max_rule_length if max_rule_length > 4 else 4
        str_template += '{:' + str(max_rule_length) + '}'
        table_width += max_rule_length

    if column_length >= 2:
        max_endpoint_length = max(len(str(r[1])) for r in rows)
        # max_endpoint_length = max(rows, key=len)
        max_endpoint_length = (
            max_endpoint_length if max_endpoint_length > 8 else 8)
        str_template += '  {:' + str(max_endpoint_length) + '}'
        table_width += 2 + max_endpoint_length

    if column_length >= 3:
        max_arguments_length = max(len(str(r[2])) for r in rows)
        max_arguments_length = (
            max_arguments_length if max_arguments_length > 9 else 9)
        str_template += '  {:' + str(max_arguments_length) + '}'
        table_width += 2 + max_arguments_length

    click.echo(str_template.format(*column_headers[:column_length]))
    click.echo('-' * table_width)

    for row in rows:
        click.echo(str_template.format(*row[:column_length]))


@click.command()
@with_appcontext
def make_users():
    """Create a couple of users to test with."""
    def is_user_available(user_email):
        if User.query.filter_by(email=user_email).first():
            return True
        else:
            return False
    # Create roles, if not yet created
    if not Role.get_role("chef"):
        db.session.add(Role(name='chef', description='Chef in the kitchen.'))
    if not Role.get_role("guest"):
        db.session.add(Role(name='guest', description='Visitor.'))
    db.session.commit()
    # Create some users
    if not is_user_available("mm.ronic@gmail.com"):
        db.session.add(User("mm.ronic@gmail.com", "password", "chef"))
    if not is_user_available("mm.ronic+guest@gmail.com"):
        db.session.add(User("mm.ronic+guest@gmail.com", "password", "guest"))
    db.session.commit()
    print("Successfully generated user roles")
    print("Successfully generated users")
