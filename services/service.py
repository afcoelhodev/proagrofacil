from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, SelectField, PasswordField, EmailField, DateField
from wtforms.validators import email_validator, DataRequired
from cpf_generator import CPF
import geopy.distance


class UserForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=1, max=50)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=1, max=250)])
    login = SubmitField('Login')


class AgroForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired(), validators.Length(min=1, max=180)])
    cpf = StringField('CPF', [validators.DataRequired(), validators.Length(min=11, max=11, message='only numbers')], description="Only numbers: 12345678910")
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    local_LAT = StringField('local_LAT', [validators.DataRequired(), validators.Length(min=10, max=10, message='formato: -12.345678')])
    local_LON = StringField('local_LON', [validators.DataRequired(), validators.Length(min=10, max=10, message='formato: -12.345678')])
    lavoura = StringField('Lavoura', [validators.DataRequired(), validators.Length(min=1, max=180)])
    colheita = StringField('Data Colheita', [validators.DataRequired(), validators.Length(min=10, max=10)])
    # colheita = DateField('Data Colheita', [validators.DataRequired()], format='%Y-%m-%d')
    causa = SelectField('Causa', [validators.DataRequired()], choices=['CHUVA EXCESSIVA', 'GEADA', 'GRANIZO', 'SECA', 'VENDAVAL', 'RAIO'])
    save = SubmitField('Save')


def validate_cpf(cpf: str) -> bool:
    check = CPF.validate(cpf)
    return check

def check_geodistance(first_lat: str, first_long: str, second_lat: str, second_lon: str) -> bool:

    geo1 = (first_lat, first_long)
    geo2 = (second_lat, second_lon)

    result = geopy.distance.distance(geo1, geo2)
    print(result)

    if result < 10:
        return False
    else:
        return True

def format_date(date: str) -> bool:
    try:
        d = list(date)
        day = int(f"{d[0]}{d[1]}")
        month = int(f"{d[3]}{d[4]}")
        year = int(f"{d[6]}{d[7]}{d[8]}{d[9]}")
        if day < 1 or day > 31:
            return False
        elif month < 1 or month > 13:
            return False
        elif year < 0:
            return False
        elif d[2] != "/" or d[5] != "/":
            return False
        else:
            return True
    except ValueError:
        return False
