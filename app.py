import os
import traceback

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import make_response
from models.database import db, Cagetory, BookMark, queryToDict
from flask_migrate import Migrate
# 登录验证
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "db", "bookmark.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("admin")
}
migrate = Migrate(app, db)
db.init_app(app)


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":

        data = db.session.query(BookMark, Cagetory).join(Cagetory).all()
        # print(queryToDict(data))
        data_dict = {}
        for bookmark, cagetory in data:
            bookmark = queryToDict(bookmark)
            cagetory = queryToDict(cagetory)
            data_dict.setdefault(cagetory['name'], [])
            data_dict[cagetory['name']].append(bookmark)
        # return jsonify(data=data_dict)
        return render_template('index.html', dataObj=data_dict)


@app.route('/admin', methods=["GET", "POST"])
@auth.login_required
def admin():
    if request.method == "GET":
        return render_template('main.html')
    # db.session.query(Company, Buyer).join(Buyer, Buyer.buyer_id == Company.id).all()

    data = db.session.query(BookMark, Cagetory).join(Cagetory).all()
    # print(queryToDict(data))
    data_list_para = []

    for bookmark, cagetory in data:
        bookmark = queryToDict(bookmark)
        cagetory = queryToDict(cagetory)

        bookmark['cagetory_name'] = cagetory['name']
        data_list_para.append(bookmark)
    res = {
        'msg': "ok",
        'code': 0,
        'data': data_list_para,
        'count': len(data_list_para),
        # 'limit': limit,
        # "totalRow": {
        #     "pay_value": 10283,
        #     "pay_type": 10283,
        #     "payer_account": 10283
        # },
    }
    return jsonify(res)


@app.route('/cate_data', methods=["POST"])
def cate_data():
    data = Cagetory.query.filter().all()

    res = {
        'msg': "ok",
        'code': 0,
        'data': queryToDict(data),
        'count': len(data),
        # 'limit': limit,
        # "totalRow": {
        #     "pay_value": 10283,
        #     "pay_type": 10283,
        #     "payer_account": 10283
        # },
    }
    return jsonify(res)


@app.route('/cate_data_select', methods=["POST"])
def cate_data_select():
    data = Cagetory.query.filter().all()

    return jsonify(queryToDict(data))


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "GET":
        return render_template('add.html')

    r = db.session.add(
        BookMark(**request.json)
    )
    try:
        db.session.commit()
        res = {
            'msg': "添加成功",
            'code': 1,
            "success": True,
            # 'data': [data for data in data],
            # 'count': len(data),
            # 'limit': limit,
            # "totalRow": {
            #     "pay_value": 10283,
            #     "pay_type": 10283,
            #     "payer_account": 10283
            # },
        }
    except Exception as e:
        if "UNIQUE" in str(e):
            error = "重复录入"
        else:
            error = str(e)
        res = {
            'msg': error,
            'code': 0,
            'success': False,
            # 'data': [data for data in data],
            # 'count': len(data),
            # 'limit': limit,
            # "totalRow": {
            #     "pay_value": 10283,
            #     "pay_type": 10283,
            #     "payer_account": 10283
            # },
        }
        pass

    return jsonify(res)


@app.route("/addcate", methods=["POST", "GET"])
def addcate():
    if request.method == "GET":
        return render_template('addcate.html')

    r = db.session.add(
        Cagetory(**request.json)
    )
    try:
        db.session.commit()
        res = {
            'msg': "添加成功",
            'code': 1,
            "success": True,

        }
    except Exception as e:
        if "UNIQUE" in str(e):
            error = "重复录入"
        else:
            error = str(e)
        res = {
            'msg': error,
            'code': 0,
            'success': False,
            # 'data': [data for data in data],
            # 'count': len(data),
            # 'limit': limit,
            # "totalRow": {
            #     "pay_value": 10283,
            #     "pay_type": 10283,
            #     "payer_account": 10283
            # },
        }
        pass

    return jsonify(res)


@app.route("/delete_bookmark/<int:_id>", methods=["POST"])
def delete_bookmark(_id):
    try:
        db.session.delete(BookMark.query.filter_by(id=_id).first())
        db.session.commit()
        res = {
            'msg': "OK",
            'success': True,
        }
    except Exception as e:
        res = {
            'msg': str(e),
            'success': False,
        }
    return jsonify(res)


@app.route("/delete_cate/<int:_id>", methods=["POST"])
def delete_cate(_id):
    try:
        db.session.delete(Cagetory.query.filter_by(id=_id).first())
        db.session.commit()
        res = {
            'msg': "OK",
            'success': True,
        }
    except Exception as e:
        res = {
            'msg': str(e),
            'success': False,
        }

    return jsonify(res)


if __name__ == "__main__":
    app.run(debug=True)
