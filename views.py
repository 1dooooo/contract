from flask import Flask, render_template, request
import collections
import json
import csv
import os

app = Flask(__name__)

from FutureContract import InFutureContract, OutFutureContract
from db_about import DBSession

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
            if data[0].get('id', None) != None:
                FC = OutFutureContract
            else:
                FC = InFutureContract
            session = DBSession()
            for d in data:
                fc = FC(**d)
                session.add(fc)
            session.commit()

    return render_template('upload.html')

@app.route('/', methods = ['GET', 'POST'])
def index(variety = None):

    if request.args:
        keys = ['郑商所', '大商所', '中金所', '上期所', '上期能源']
        if request.args['location'] in keys:
            contracts = DBSession().query(InFutureContract).filter(InFutureContract.product == request.args['variety']).first().to_dict()
        else:
            contracts = DBSession().query(OutFutureContract).filter(OutFutureContract.product == request.args['variety']).first().to_dict()
        return render_template('contract.html', contracts = contracts)


    # return render_template('contract.html', contracts = DBSession().query(InFutureContract).first().to_dict())
    context = collections.defaultdict(list)
    fcs = DBSession().query(InFutureContract, InFutureContract.exchange, InFutureContract.product)
    for fc in fcs:
        context[fc.exchange].append(fc.product)
    fcs = DBSession().query(OutFutureContract, OutFutureContract.exchange, OutFutureContract.product)
    for fc in fcs:
        if fc.exchange.startswith('美国洲际交易所'):
            context['美国洲际交易所'].append(fc.product)
            continue
        if fc.exchange.startswith('芝加哥商业交易所'):
            context['芝加哥商业交易所'].append(fc.product)
            continue
        context[fc.exchange].append(fc.product)

    map_dict = {'上海国际能源交易中心':'上期能源', '上海期货交易所':'上期所', '郑州商品交易所':'郑商所','大连商品交易所':'大商所','中金所':'中金所','芝加哥商业交易所':'CME','欧洲期货交易所':'EUREX','香港交易所':'HKEX','美国洲际交易所':'ICE','伦敦金属交易所':'LME','新加坡交易所':'SGX','东京商品交易所':'TOCOM','马来西亚交易所':'MYX'}
    tmp_dict = {}
    for c in context:    
        if c in map_dict:
            tmp_dict[map_dict[c]] = context[c]
        elif c == '':
            tmp_dict['(未知所)'] = context[c]
        else:
            tmp_dict[c] = context[c]
    context = tmp_dict

    return render_template('tabbar.html', context = context)

@app.route('/add_in', methods=['POST', 'GET'])
def add_in():
    if request.method == 'POST':
        ifc = InFutureContract(**{key: request.form[key] for key in request.form})
        session = DBSession()
        session.add(ifc)
        session.commit()

    return render_template('add_in.html')
@app.route('/add_out', methods=['POST', 'GET'])
def add_out():
    if request.method == 'POST':
        ifc = OutFutureContract(**{key: request.form[key] for key in request.form})
        session = DBSession()
        session.add(ifc)
        session.commit()
    return render_template('add_out.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0')
