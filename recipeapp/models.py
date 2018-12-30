# -*- coding: utf-8 -*-
from extensions import db, bcrypt
from flask_security import UserMixin, RoleMixin

# User to role mapping
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
)


class Role(db.Model, RoleMixin):
    __tablename__ = "roles"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return str(self.name)

    @staticmethod
    def get_role(role):
        role = Role.query.filter_by(name=role).first()
        if role:
            return role
        else:
            return None


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(120))
    active = db.Column(db.Boolean())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __init__(self, email, password, role):
        self.email = email
        self.active = True
        self.password = User.hashed_password(password)
        user_role = Role.get_role(role)
        if user_role:
            self.roles.append(user_role)

    @staticmethod
    def hashed_password(password):
        return bcrypt.generate_password_hash(password).decode("utf-8")

    @staticmethod
    def get_user_with_email_and_password(user_email, user_password):
        user = User.query.filter_by(email=user_email).first()
        if user and bcrypt.check_password_hash(user.password, user_password):
            return user
        else:
            return None

    def is_active(self):
        return self.active

    def is_anonymous(self):
        if not self.roles or 'Guest' in self.roles:
            return True

    def get_id(self):
        return self.id

    def is_user(self, user_email):
        user = User.query.filter_by(email=user_email).first()
        if user:
            return True
        else:
            return False

    def __repr__(self):
        return "{0} {1}".format(self.first_name, self.last_name)
