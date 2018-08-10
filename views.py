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
            session.close()

    return render_template('upload.html')


@app.route('/show', methods = ['GET', 'POST'])
def show(variety = None):
    if request.args:
        variety = request.args['variety']
        location = request.args['location']
        contracts = DBSession().query(FutureContract).filter(FutureContract.product == variety, FutureContract.exchange.like(location+'%')).first().to_dict()
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


@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        fc = FutureContract(**{key: request.form[key] for key in request.form})
        session = DBSession()
        session.add(fc)
        session.commit()
        session.close()
    return render_template('add.html')

@app.route('/search', methods=['POST'])
def search():
    fcs = collections.defaultdict(list)
    keyword = request.form['keyword']
    for fc in DBSession().query(FutureContract.exchange, FutureContract.product).filter(FutureContract.product.like("%"+keyword+"%")).all():
        if fc.exchange.startswith('美国洲际交易所'):
            fcs['美国洲际交易所'].append(fc[1])
            continue
        if fc.exchange.startswith('芝加哥商业交易所'):
            fcs['芝加哥商业交易所'].append(fc[1])
            continue
        fcs[fc[0]].append(fc[1])
    return json.dumps(fcs)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.args:
        variety = request.args['variety']
        location = request.args['location']
        contracts = DBSession().query(FutureContract).filter(FutureContract.product == variety, FutureContract.exchange.like(location+'%')).first().to_dict()
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
    fc = session.query(FutureContract).filter(FutureContract.product == product, FutureContract.exchange.like(exchange+'%')).first()
    session.delete(fc)
    session.commit()
    session.close()
    return json.dumps({'ok':1})

@app.route('/modify', methods=['POST','GET'])
def modify():
    product = request.args['variety']
    exchange = request.args['location']
    global modify_fc
    session = DBSession()
    modify_fc = session.query(FutureContract).filter(FutureContract.product == product, FutureContract.exchange.like(exchange+'%')).first()
    session.commit()
    context = modify_fc.to_raw_dict()
    session.close()
    return render_template('modify.html', context = context)

@app.route('/update', methods=['POST'])
def update():
    fc = FutureContract(**{key: request.form[key] for key in request.form})
    session = DBSession()
    session.delete(modify_fc)
    session.add(fc)
    session.commit()
    session.close()
    return json.dumps({'OK':1})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
