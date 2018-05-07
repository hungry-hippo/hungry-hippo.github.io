# encoding=utf-8
# setting the required parameters for accessing the database
_database_settings = {
    'host': 'localhost',
    'port': '3306',
    'username': 'root',
    'password': '',
    'database': 'mydb',
    # http://docs.sqlalchemy.org/en/latest/dialects/mysql.html#unicode

}

SECRET_KEY = 'asdfasdfasdf'  # generate with os.urandom(32), used for session keys and such
WTF_SECRET_KEY = 'fdsafdsafdsa'  # generate with os.urandom(32), used for CSRF tokens
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{username}:{password}@{host}/{database}'.format(**_database_settings)

# Database optimisations for regular usage
SQLALCHEMY_TRACK_MODIFICATIONS = False
