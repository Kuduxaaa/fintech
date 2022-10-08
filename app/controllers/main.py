import os
from urllib import response
import config
import json
import uuid

from flask import (
    Blueprint, render_template, request, jsonify, make_response, redirect
)

from app.service import search_with_vin, vin_code

from datetime import datetime
from werkzeug.utils import secure_filename
from app.models import Orders

from flask_login import LoginManager, UserMixin, login_required
from app import login_manager
import hashlib

bp = Blueprint('main', __name__)


class User(UserMixin):
    user_database = {"admin": (
        "admin", "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9")}

    def __init__(self, username, password):
        self.id = username
        self.password = password

    @classmethod
    def get(cls, id):
        return cls.user_database.get(id)


@bp.route('/', methods=['GET', 'POST'])
def index():
    """
    Index page.
    :return: The response.
    """

    return render_template('main/index.html')


@bp.route('/order', methods=['GET', 'POST'])
def order():
    """
    Index page.
    :return: The response.
    """

    data = {}
    if request.method == 'POST':
        for required in ['brand', 'year', 'brandModel', 'vinCode', 'plateNumber', 'techPassportNo', 'phone_number']:
            if required not in request.form or request.form[required] == '0' or request.form[required] == '':
                return 'აუცილებელია ყველა ველის შევსება', 400

            data[required] = request.form.get(required)

        files = request.files.getlist('files[]')
        files_arr = []

        if files is not None and len(files) > 0:
            for file in files:
                file_name = str(uuid.uuid4()) + str(file.filename)
                file.save(os.path.join(
                    os.path.dirname(__file__),
                    '../',
                    config.Config.UPLOAD_FOLDER,
                    file_name
                ))

                files_arr.append(f'public/uploads/{file_name}')

        files_to_db = json.dumps(files_arr)
        order = Orders(
            data['brand'],
            data['year'],
            data['brandModel'],
            data['vinCode'],
            data['plateNumber'],
            data['techPassportNo'],
            data['phone_number'],
            files_to_db
        )

        order.save()
        return '<script>alert("თქვენი მოთხოვნა წარმატებით გაიგზავნა და მუშავდება");window.history.back(-1);</script>'

    return render_template('main/loan.html', year=datetime.now().year)


@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    response = make_response(redirect('/'))
    response.delete_cookie('auth_token')
    return response


@bp.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    orders = [{
        'id': o.id,
        'uuid': o.uuid,
        'brand': o.brand,
        'year': o.year,
        'model': o.model,
        'vin_code': o.vin_code,
        'plate_number': o.plate_number,
        'tech_passport_number': o.tech_passport_number,
        'phone_number': o.phone_number,
        'files': o.files,

    } for o in Orders.query.all()]
    if request.method == 'POST':
        pass

    return render_template('main/admin.html', orders=orders)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'username' not in request.form or 'password' not in request.form \
                or len(request.form['username']) <= 0 or len(request.form['password']) <= 0:
            return 'გთხოოვთ შეავსოთ ყველა მოცემული ველი'

        u = User.get(request.form['username'])
        if u is not None:
            user = User(u[0], u[1])
            pwd = hashlib.sha256(request.form['password'].encode()).hexdigest()

            if (user.password == pwd):
                response = make_response(redirect('/admin'))
                response.set_cookie(
                    'auth_token', request.form['username'] + ':' + pwd)
                return response

        return 'მომხმარებლის პაროლი ან სახელი არასწორია'

    return render_template('main/login.html')


@login_manager.request_loader
def load_user(request):
    token = request.cookies.get('auth_token')
    if token is None:
        token = request.args.get('token')

    if token is not None:
        username, password = token.split(":")  # naive token
        user_entry = User.get(username)
        if (user_entry is not None):
            user = User(user_entry[0], user_entry[1])
            if (user.password == password):
                return user

    return None


@bp.route('/admin/details/<order_id>')
@login_required
def order_details(order_id):
    order = Orders.query.filter_by(id=order_id).first()
    if order is not None:
        vim_results = search_with_vin(order.vin_code)
        return render_template('main/details.html', order={
            'id': order.id,
            'uuid': order.uuid,
            'brand': order.brand,
            'year': order.year,
            'model': order.model,
            'vin_code': order.vin_code,
            'plate_number': order.plate_number,
            'tech_passport_number': order.tech_passport_number,
            'phone_number': order.phone_number,
            'files': json.loads(order.files),
        }, vin=vim_results)


    else:
        return 'მსგავსი ორდერი ვერ მოიძებნა!'
