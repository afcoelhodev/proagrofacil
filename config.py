from flask import Flask

SECRET_KEY = 'proagro'

config_mysql = {
    'SGBD': 'mysql+mysqlconnector',
    'user': 'user',
    'password': 'password',
    'server': 'localhost',
    'port': '3306',
    'database': 'agro_db'
}

SQLALCHEMY_DATABASE_URI = f"{config_mysql['SGBD']}://" \
                                        f"{config_mysql['user']}:{config_mysql['password']}@{config_mysql['server']}:" \
                                        f"{config_mysql['port']}/{config_mysql['database']}"

SQLALCHEMY_TRACK_MODIFICATIONS = False
