from flask import Flask, render_template, request
import collections
import json
import csv
import os

app = Flask(__name__)

from FutureContract import FutureContract
from db_about import DBSession

@app.route('/', methods = ['GET', 'POST'])
@app.route('/admin', methods = ['GET', 'POST'])
def admin():
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

    return render_template('add_in.html')

@app.route('/search', methods=['POST'])
def search():
    fcs = []
    keyword = request.form['keyword']
    fcs = [{'product':fc[0], 'exchange':fc[1]} for fc in DBSession().query(FutureContract.product, FutureContract.exchange).filter(FutureContract.product.like("%"+keyword+"%")).all()]
    return json.dumps(fcs)

<<<<<<< HEAD
=======
@app.route('/delete', methods=['POST'])
def delete():
    status = ""

    return status

@app.route('/modify', methods=['POST'])
def modify():
    status = ""
    
    return status
>>>>>>> dcc7c2fa2204f28863a7ba8f34bd8a412f491737

if __name__ == '__main__':
    app.run(host='0.0.0.0')
