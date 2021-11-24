import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
  
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'QualitelHelpDesk'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://localadmin:um8%JKid#G6N8ep2@localhost/helpdesk'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # 1MB max-limit.




    # MAIL:
    # MAIL_SERVER = 'smtp.office365.com'
    # MAIL_PORT = 587
    # MAIL_USERNAME = 'hillarym@qualitel.net'
    # MAIL_PASSWORD = 'Nightwing!13'
    # MAIL_USE_TLS = True
    # MAIL_USE_SSL = False

    # MAIL_SERVER='smtp.mailtrap.io'
    # MAIL_PORT=2525
    # MAIL_USERNAME='6f97b25e586226'
    # MAIL_PASSWORD='5a66fac992bc94'
    # MAIL_USE_TLS=True
    # MAIL_USE_SSL=False

    MAIL_SERVER = '10.1.10.120'
    MAIL_PORT=25
    # MAIL_USERNAME='engineeringtickets@qualitel.net'
    # MAIL_PASSWORD=
    MAIL_USE_TLS=False
    MAIL_USE_SSL=False