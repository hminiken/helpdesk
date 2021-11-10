import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # ...
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'QualitelHelpDesk'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:jupiter5@localhost/helpdesk'
    # SQLALCHEMY_BINDS = {
    #     'erp':      'mssql+pyodbc://zachd:1716@QEA-ERP805.QEA.local\iERP90,1436:1436/iERP807?driver=ODBC+Driver+17+for+SQL+Server'
    # }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

# engine = create_engine(
#     "mssql+pyodbc://scott:tiger@myhost:port/databasename?driver=ODBC+Driver+17+for+SQL+Server")
