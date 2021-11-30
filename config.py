import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
  
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'QualitelHelpDesk'
    SECRET_KEY = 'MYNEWSECRETKEY'
    WTF_CSRF_SECRET_KEY = 'MYNEWSECRETKEY'
    SESSION_COOKIE_SECURE = False

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://localadmin:um8%JKid#G6N8ep2@localhost/helpdesk'
    # SQLALCHEMY_BINDS = {
    #                     'db3': 'mysql+pymysql://localadmin:um8%JKid#G6N8ep2@localhost/dailyids'
    #                     }

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # 1MB max-limit.

    MAIL_SERVER = '10.1.10.120'
    MAIL_PORT=25
    MAIL_USE_TLS=False
    MAIL_USE_SSL=False
    WTF_CSRF_ENABLED = True


    # MAY OR MAY NOT NEED THIS TO FIX THE CSRF ERROR
    # SERVER_NAME = 'qea-engineeringtickets:5000'
