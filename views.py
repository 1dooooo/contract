from flask import Flask, render_template, request
import collections
import json
import csv
import os
from urllib import parse

app = Flask(__name__)

from FutureContract import FutureContract
from db_about import DBSession

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        for file in request.files:
            f = request.files[file]
            post_fix = f.filename.rsplit('.', 1)[1]
            if post_fix == 'csv':
                f.save('/tmp/' + f.filename)
                with open('/tmp/' + f.filename, 'r', encoding = 'utf-8') as file:
                    data = csv.DictReader(file)
                    data = [dict(d) for d in data]
                os.remove('/tmp/'+f.filename)

            if post_fix == 'json':
                data = json.load(f)
            session = DBSession()
            for d in data:
                fc = FutureContract(**d)
                session.add(fc)
            session.commit()

    return render_template('upload.html')


@app.route('/show', methods = ['GET', 'POST'])
def show(variety = None):
    if request.args:
        variety = request.args['variety']
        location = request.args['location']
        contracts = DBSession().query(FutureContract).filter(FutureContract.product == variety, FutureContract.exchange == location).first().to_dict()
        return render_template('contract.html', contracts = contracts)

    context = collections.defaultdict(list)
    fcs = DBSession().query(FutureContract, FutureContract.exchange, FutureContract.product)
    for fc in fcs:
        if fc.exchange.startswith('美国洲际交易所'):
            context['美国洲际交易所'].append(fc.product)
            continue
        if fc.exchange.startswith('芝加哥商业交易所'):
            context['芝加哥商业交易所'].append(fc.product)
            continue
        context[fc.exchange].append(fc.product)
    return render_template('tabbar.html', context = context)


@app.route('/add_in', methods=['POST', 'GET'])
def add_in():
    if request.method == 'POST':
        fc = FutureContract(**{key: request.form[key] for key in request.form})
        session = DBSession()
        session.add(fc)
        session.commit()
    tester = DBSession().query(FutureContract).filter(FutureContract.product == '白银').first().to_raw_dict()
    return render_template('add_in.html', context=tester)

@app.route('/search', methods=['POST'])
def search():
    fcs = []
    keyword = request.form['keyword']
    fcs = [{'product':fc[0], 'exchange':fc[1]} for fc in DBSession().query(FutureContract.product, FutureContract.exchange).filter(FutureContract.product.like("%"+keyword+"%")).all()]
    return json.dumps(fcs)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.args:
        variety = request.args['variety']
        location = request.args['location']
        contracts = DBSession().query(FutureContract).filter(FutureContract.product == variety, FutureContract.exchange == location).first().to_dict()
        return render_template('contract.html', contracts = contracts)

    context = collections.defaultdict(list)
    fcs = DBSession().query(FutureContract, FutureContract.exchange, FutureContract.product)
    for fc in fcs:
        if fc.exchange.startswith('美国洲际交易所'):
            context['美国洲际交易所'].append(fc.product)
            continue
        if fc.exchange.startswith('芝加哥商业交易所'):
            context['芝加哥商业交易所'].append(fc.product)
            continue
        context[fc.exchange].append(fc.product)
    return render_template('admin.html',context=context)


@app.route('/delete', methods=['POST'])
def delete():
    data_dict = {}
    data = request.form['data']
    data = parse.unquote(data)
    lst = data.split('&')
    for exp in lst:
        e = exp.split('=')
        data_dict[e[0]] = e[1]

    product = data_dict['variety']
    exchange = data_dict['location']
    session = DBSession()
    session.query(FutureContract).filter(FutureContract.product == product, FutureContract.exchange == exchange).delete()
    session.commit()
    return json.dumps({'ok':1})

@app.route('/modify', methods=['POST'])
def modify():
    product = request.form['product']
    exchange = request.form['exchange']
    context = DBSession().query(FutureContract).filter(FutureContract.product == product, FutureContract.exchange == exchange).all().to_raw_dict()

    return render_template('add_in.html', context = context)

@app.route('/update', methods=['POST'])
def update():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0')
