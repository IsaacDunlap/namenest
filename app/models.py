# Data models for the NameNest application and related functions.
#
# Classes:
#   Role - represents a user role. Different roles have different
#          permissions.
#   User - represents a user of NameNest.
#
# Functions:
#   load_user - loads a user for a given id value.

from flask import current_app
from flask.ext.login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager


class Role(db.Model):
    # Represents a user role (e.g. administrator, user, moderator,
    # etc.). A role is identified by its name and its id.
    #
    # Inherits from the database Model class.
    #
    # Class variables:
    #   ---------- PUBLIC ----------
    #   id (Column) - an integer database column for the id value.
    #   name (Column) - a string database column for the name.
    #   users (RelationshipProperty) -
    #       a back-reference to the users with the given role. This is
    #       a dynamic relationship.
    #   ---------- PRIVATE ----------
    #   __tablename__ (string) - the name of the database table.
    #
    # Methods:
    #   ---------- PRIVATE ----------
    #   __repr__ - returns a representation of a Role instance.

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        # Do not include the id value since the id value isn't
        # meaningful to a user of our class.
        return 'Role <%r>' % self.name


class User(UserMixin, db.Model):
    # Represents a user of NameNest. A user is identified by its
    # username and id.
    #
    # Inherits from the UserMixin and database Model classes.
    #
    # Class variables:
    #   ---------- PUBLIC ----------
    #   id (Column) - an integer database column for the id value.
    #   username (Column) - a string database column for the username.
    #   email (Column) - a string database column for the email address.
    #   role_id (Column) - an integer database column for the
    #                      corresponding role's id value.
    #   password_hash (Column) - a string database column for the hash
    #                            of the user's password.
    #   ---------- PRIVATE ----------
    #   __tablename__ (string) - the name of the database table.
    #
    # Attributes:
    #   ---------- WRITE-ONLY ----------
    #   password (string) - the user's password.
    #
    # Methods:
    #   ---------- PUBLIC ----------
    #   verify_password - checks a provided password against the user's
    #                     stored password hash.
    #   ---------- PRIVATE ----------
    #   __repr__  (override) - returns a representation of a User instance.

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(length=128))
    confirmed = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        # This attribute is a string (or can be bytes). It is write-
        # only. Setting this attribute stores a hash of the password in
        # the application database. Getting this attribute is denied.
        #
        # Raises:
        #   AttributeError - always, since password is a write-only
        #                    attribute.

        raise AttributeError('password is a write-only attribute')

    @password.setter
    def password(self, password):
        # Arguments:
        #   password (string) -
        #       the user's password. Do not validate it here - it
        #       should be verified by the server before being set. The
        #       password can be other types that can be converted into
        #       bytes.
        #
        # Raises:
        #   TypeError - when the password cannot be hashed.

        try:
            self.password_hash = generate_password_hash(password)
        except TypeError:
            raise TypeError('cannot hash a %s type' % type(password).__name__)

    def __repr__(self):
        # Do not include the id value since the id value isn't
        # meaningful to a user of our class.
        return 'User <%r>' % self.username

    def verify_password(self, password):
        # Check that the supplied password has the same hash as the
        # password_hash attribute.
        #
        # Arguments:
        #   password (string) - the password we wish to verify. This
        #                       can be other types that can be
        #                       converted into bytes.
        #
        # Returns:
        #   (boolean) - True if the password has the same has as the
        #               password_hash attribute, and false otherwise.
        #
        # Raises:
        #   TypeError - when the supplied password cannot be hashed.

        try:
            password_is_correct = check_password_hash(self.password_hash, password)
        except TypeError:
            raise TypeError('cannot hash a %s type' % type(password).__name__)

        return password_is_correct


@login_manager.user_loader
def load_user(user_id):
    # Load the user with the given user id.
    #
    # Arguments:
    #   user_id (int) - the user id value, which can be any type that
    #                   can be converted into an integer.
    #
    # Returns:
    #   (User) - the user with the id value, or None if not found.
    #
    # Raises:
    #   RuntimeError - when working outside the application context or
    #                  when there is no database used by the app.

    return User.query.get(int(user_id))
