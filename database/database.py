# Configurate the main database for the flask application

import sqlalchemy as sqldb
import sqlalchemy.orm
import mysql.connector
from models.models import Users_db, Base
from flask_bcrypt import generate_password_hash


class Connection_db:
    def __init__(self):
        self.engine = sqldb.create_engine(
            'mysql+mysqlconnector://user:password@127.0.0.1:3306/agro_db'
        )
        self.engine.connect()

    def create_session(self):
        self.Session = sqlalchemy.orm.sessionmaker()
        self.Session.configure(bind=self.engine)
        self.session = self.Session()
        return self.session


class Proagro_db:
    def __init__(self):
        self.conn = Connection_db()
        self.session = self.conn.create_session()

    def creating_db(self):
        Base.metadata.create_all(self.conn.engine)

        print('database initialization finish\n')
        print('+-' * 30, '\n')
        print('saving main user to Users database\n')

        main_user = [
            ('softfocus', generate_password_hash("soft@22").decode('utf-8'))
        ]

        for user in main_user:
            new_user = Users_db(
                username=f"{user[0]}",
                password=f"{user[1]}"
            )
            self.session.add(new_user)
            self.session.commit()

        print('databases tables created and main user registered\n')
        print('+-' * 30, '\n')

if __name__ == '__main__':
    app_db = Proagro_db()
    app_db.creating_db()    # run only once for start the application database
