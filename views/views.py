# Declaring all the routes on the flask application

from flask import Flask, render_template, request, redirect, session, flash, url_for
from app import app
from database.database import Connection_db, Proagro_db
from services.service import UserForm, AgroForm, validate_cpf, check_geodistance, format_date
from models.models import Agro_db, Users_db
from flask_bcrypt import check_password_hash


db_manager = Agro_db()

@app.route('/')
def index():
    conn = Connection_db()
    db_session = conn.create_session()
    lista = db_session.query(Agro_db).order_by(Agro_db.id).all()
    form = AgroForm()
    return render_template('home.html', header_title='Agro Manager', agro_list=lista, form=form)


@app.route('/consult', methods=['GET', 'POST'])
def consult():
    if 'logged_user' not in session or session['logged_user'] is None:
        return redirect(url_for('login', nexturl=url_for('new')))

    if request.method == "POST":
        conn = Connection_db()
        db_session = conn.create_session()

        cpf = request.form['buscaCPF']

        if validate_cpf(cpf) is False:
            flash("CPF does not exist/incorrect")
            return redirect(url_for('index'))

        reg_list = db_session.query(Agro_db).filter_by(cpf=cpf).all()
        reg_list_count = db_session.query(Agro_db).filter_by(cpf=cpf).count()

        if reg_list_count == 0:
            flash("CPF does not match with any communication on database. Please try again.")
        else:
            flash("Successfully consulted!")
            return render_template('consult.html', header_title='Agro Manager', reg_list=reg_list)


@app.route('/new')
def new():
    if 'logged_user' not in session or session['logged_user'] is None:
        return redirect(url_for('login', nexturl=url_for('new')))

    agro_form = AgroForm()
    return render_template('new.html', header_title='New Register', form=agro_form)

@app.route('/create', methods=['POST'])
def create():
    form = AgroForm(request.form)

    if not form.validate_on_submit():
        flash("Information provided are incorrectly. Please check again.")
        return redirect(url_for('new'))

    name = form.name.data
    cpf = form.cpf.data
    email = form.email.data
    local_LAT = form.local_LAT.data
    local_LON = form.local_LON.data
    lavoura = form.lavoura.data
    colheita = form.colheita.data
    causa = form.causa.data

    if validate_cpf(cpf) is False:
        flash("CPF does not exist/incorrect")
        return redirect(url_for('new'))

    elif format_date(colheita) is False:
        flash("Incorrect date format. Please use date format as dd/mm/yyyy")
        return redirect(url_for('new'))

    else:
        conn = Connection_db()
        db_session = conn.create_session()

        historic_count = db_session.query(Agro_db).filter_by(cpf=cpf).count()
        historic = db_session.query(Agro_db).filter_by(cpf=cpf).all()

        if historic_count == 0:

            new_reg = Agro_db(
                name=name,
                cpf=cpf,
                email=email,
                local_LAT=local_LAT,
                local_LON=local_LON,
                lavoura=lavoura,
                colheita=colheita,
                causa=causa,
            )
            db_session.add(new_reg)
            db_session.commit()

            flash("Communication registered with success")
            return redirect(url_for('index'))

        else:

            for item in historic:
                c1_lat = item.local_LAT
                c1_lon = item.local_LON
                check_causa = item.causa

                if check_geodistance(c1_lat, c1_lon, local_LAT, local_LON) is False:
                    if check_causa == causa:
                        flash("Registration denied - Already have a similar communication with same cause in the region - CONTACT PRODUCTOR")
                        return redirect(url_for('index'))
                    else:
                        flash("Registration denied - Already have a similar communication with different cause in the region - CONTACT PRODUCTOR")
                        return redirect(url_for('index'))

            new_reg = Agro_db(
                name=name,
                cpf=cpf,
                email=email,
                local_LAT=local_LAT,
                local_LON=local_LON,
                lavoura=lavoura,
                colheita=colheita,
                causa=causa,
            )
            db_session.add(new_reg)
            db_session.commit()

            flash("Communication registered with success")
            return redirect(url_for('index'))


@app.route('/edit/<int:id>')
def edit(id):
    if 'logged_user' not in session or session['logged_user'] is None:
        return redirect(url_for('login', nexturl=url_for('new')))

    conn = Connection_db()
    db_session = conn.create_session()

    reg = db_session.query(Agro_db).filter_by(id=id).first()

    form = AgroForm()
    form.name.data = reg.name
    form.cpf.data = reg.cpf
    form.email.data = reg.email
    form.local_LAT.data = reg.local_LAT
    form.local_LON.data = reg.local_LON
    form.lavoura.data = reg.lavoura
    form.colheita.data = reg.colheita
    form.causa.data = reg.causa

    return render_template('update.html', id=id, form=form)


@app.route('/update', methods=['POST'])
def update():
    form = AgroForm(request.form)

    if form.validate_on_submit():
        conn = Connection_db()
        db_session = conn.create_session()
        reg = db_session.query(Agro_db).filter_by(id=request.form['id']).first()
        reg.name = form.name.data
        reg.cpf = form.cpf.data
        reg.email = form.email.data
        reg.local_LAT = form.local_LAT.data
        reg.local_LON = form.local_LON.data
        reg.lavoura = form.lavoura.data
        reg.colheita = form.colheita.data
        reg.causa = form.causa.data

        db_session.add(reg)
        db_session.commit()

        flash("Communication updated with success")
        return redirect(url_for('index'))
    else:
        flash('Updated not completed/wrong data - try again')
        return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete(id):
    if 'logged_user' not in session or session['logged_user'] is None:
        return redirect(url_for('login', nexturl=url_for('new')))

    conn = Connection_db()
    db_session = conn.create_session()

    reg = db_session.query(Agro_db).filter_by(id=id).first()
    reg_name = reg.name

    db_session.delete(reg)
    db_session.commit()

    flash(f'Registration for {reg_name} successfully deleted')
    return redirect(url_for('index'))


@app.route('/login')
def login():
    nexturl = request.args.get('nexturl')
    user_form = UserForm()
    return render_template('login.html', nexturl=nexturl, form=user_form)


@app.route('/authentication', methods=["POST"])
def authentication():
    form = UserForm(request.form)

    conn = Connection_db()
    db_session = conn.create_session()

    user = db_session.query(Users_db).filter_by(username=request.form['username']).first()
    password = check_password_hash(user.password, form.password.data)
    if user and password:
        session['logged_user'] = user.username
        flash(user.username + ' successfully logged in')
        next_url = request.form['nexturl']
        return redirect(next_url)
    else:
        flash('User not found/incorrect')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['logged_user'] = None
    flash('Logout successfully')
    return redirect(url_for('index'))