import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Load local secrets (database password etc.) from .env, which git ignores
_env_path = os.path.join(basedir, '.env')
if os.path.exists(_env_path):
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith('#') and '=' in _line:
                _key, _value = _line.split('=', 1)
                os.environ.setdefault(_key.strip(), _value.strip())


class Config(object):
  
    # TO DO: Update to not hardcode in the secret key
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'QualitelHelpDesk'
    SECRET_KEY = 'MYNEWSECRETKEY'
    WTF_CSRF_SECRET_KEY = 'MYNEWSECRETKEY'
    SESSION_COOKIE_SECURE = False

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # SQLALCHEMY_BINDS = {
    #                     'db3': 'mysql+pymysql://<user>:<password>@localhost/dailyids'
    #                     }

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = '10.1.10.120'
    MAIL_PORT=25
    MAIL_USE_TLS=False
    MAIL_USE_SSL=False
    WTF_CSRF_ENABLED = True


    # MAY OR MAY NOT NEED THIS TO FIX THE CSRF ERROR
    # SERVER_NAME = 'qea-engineeringtickets:5000'
