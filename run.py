import pymysql
from app import app

pymysql.install_as_MySQLdb()

if __name__ == '__main__':
    app.run()