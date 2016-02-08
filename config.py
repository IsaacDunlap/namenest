import os


class Config:
    # Describes the universal configuration for all NameNest apps.
    # More specific configurations can be specified by subclassing this
    # class.
    #
    # Class constants:
    #   ---------- PUBLIC ----------
    #   SECRET_KEY (string) - Used as an encryption key by Flask.
    #   SQLALCHEMY_COMMIT_ON_TEARDOWN (boolean) -
    #       Whether or not to commit database changes at the end of each
    #       request.
    #   NAMENEST_MAIL_SUBJECT_PREFIX (string) -
    #       Prefix in front of the subject of all NameNest emails.
    #   NAMENEST_MAIL_SENDER (string) -
    #       Email address NameNest applications are sent from.
    #   NAMENEST_ADMIN (string) - Email address of the NameNest administrator.
    #
    # Methods:
    #   ---------- PUBLIC ----------
    #   init_app - hook for initializing the an app according to the
    #              class's configuration.

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    NAMENEST_MAIL_SUBJECT_PREFIX = '[NameNest]'
    NAMENEST_MAIL_SENDER = 'NameNest Admin <namenest@gmail.com>'
    NAMENEST_ADMIN = os.environ.get('NAMENEST_ADMIN') or 'namenest.admin@gmail.com'

    @staticmethod
    def init_app(app):
        # A hook method.
        pass


class DevelopmentConfig(Config):
    # The configuration for a development setting. This is the default
    # configuration for NameNest.
    #
    # Inherits from the Config class.
    #
    # Class constants:
    #   ---------- PUBLIC ----------
    #   DEBUG (boolean) - Flags whether debug mode is on or off.
    #   SQLALCHEMY_DATABASE_URI (string) -
    #       The URI of the NameNest development database.

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql+pymysql://NameNest:password@localhost:3307/namenestdev'


class TestingConfig(Config):
    # The configuration for testing.
    #
    # Inherits from the Config class.
    #
    # Class constants:
    #   ---------- PUBLIC ----------
    #   TESTING (boolean) - Flags whether testing mode is on or off.
    #   SQLALCHEMY_DATABASE_URI (string) -
    #       The URI of the NameNest test database.
    #   WTF_CSRF_ENABLED (boolean) - Whether CSRF protection is enabled or not.

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'mysql+pymysql://NameNest:password@localhost:3307/namenesttest'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    # The configuration for when the app is deployed.
    #
    # Inherits from the Config class.
    #
    # Class constants:
    #   ---------- PUBLIC ----------
    #   SQLALCHEMY_DATABASE_URI (string) -
    #       The URI of the NameNest test database.

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://NameNest:password@localhost:3307/namenest'


# This is used to make command line calls possible. The configuration
# desired is specified with the key, which causes the corresponding
# configuration value to be used.
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
