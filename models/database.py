# -*- coding: utf-8 -*-
# @Time    : 2022/7/26 11:48
# @Author  : Zac
# @Email   : aiguagu3041140346@163.com
# @File    : database.py
# @Software: PyCharm

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class Cagetory(db.Model):
    id = db.Column(db.Integer, primary_key=True, comment="ID")
    remark = db.Column(db.Text, comment="备注")
    create_at = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')

    name = db.Column(db.String(255), unique=True, nullable=False)


class BookMark(db.Model):
    id = db.Column(db.Integer, primary_key=True, comment="ID")
    remark = db.Column(db.Text, comment="备注")
    create_at = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')

    cagetory_id = db.Column(db.Integer, db.ForeignKey(Cagetory.id))
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), unique=True, nullable=False)
    img = db.Column(db.String(255), default='e.png', nullable=False)
    desc = db.Column(db.String(255), nullable=False)


from datetime import datetime as cdatetime  # 有时候会返回datatime类型
from datetime import date, time
from flask_sqlalchemy import Model
from sqlalchemy.orm.query import Query
from sqlalchemy import DateTime, Numeric, Date, Time  # 有时又是DateTime


def queryToDict(models):
    if (isinstance(models, list)):
        if len(models) == 0:
            return []
        if (isinstance(models[0], Model)):
            lst = []
            for model in models:
                gen = model_to_dict(model)
                dit = dict((g[0], g[1]) for g in gen)
                lst.append(dit)
            return lst
        else:
            res = result_to_dict(models)
            return res
    else:
        if (isinstance(models, Model)):
            gen = model_to_dict(models)
            dit = dict((g[0], g[1]) for g in gen)
            return dit
        else:
            res = dict(zip(models.keys(), models))
            find_datetime(res)
            return res


# 当结果为result对象列表时，result有key()方法
def result_to_dict(results):
    res = [dict(zip(r.keys(), r)) for r in results]
    # 这里r为一个字典，对象传递直接改变字典属性
    for r in res:
        find_datetime(r)
    return res


def model_to_dict(model):  # 这段来自于参考资源
    for col in model.__table__.columns:
        if isinstance(col.type, DateTime):
            value = convert_datetime(getattr(model, col.name))
        elif isinstance(col.type, Numeric):
            value = float(getattr(model, col.name))
        else:
            value = getattr(model, col.name)
        yield (col.name, value)


def find_datetime(value):
    for v in value:
        if (isinstance(value[v], cdatetime)):
            value[v] = convert_datetime(value[v])  # 这里原理类似，修改的字典对象，不用返回即可修改


def convert_datetime(value):
    if value:
        if (isinstance(value, (cdatetime, DateTime))):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        elif (isinstance(value, (date, Date))):
            return value.strftime("%Y-%m-%d")
        elif (isinstance(value, (Time, time))):
            return value.strftime("%H:%M:%S")
    else:
        return ""
