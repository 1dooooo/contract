from flask import Flask, render_template, request, jsonify
from flask_restful import Api, Resource
from FutureContract import FutureContract
from db_about import DBSession
from urllib import parse

import collections, json, csv, os


app = Flask(__name__)
api = Api(app)


class FcListApi(Resource):
    def get(self):
        context = collections.defaultdict(list)
        fcs = DBSession().query(FutureContract).all()
        for fc in fcs:
            if fc.exchange.startswith('美国洲际交易所'):
                context['美国洲际交易所'].append(fc.product)
                continue
            if fc.exchange.startswith('芝加哥商业交易所'):
                context['芝加哥商业交易所'].append(fc.product)
                continue
            context[fc.exchange].append(fc.product)
        return jsonify(context)
    def post(self):
        fc = FutureContract(**{key: request.form[key] for key in request.form})
        session = DBSession()
        session.add(fc)
        session.commit()
        session.close()
        return {'ok': 1}

class FcApi(Resource):
    def get(self, var, loc):
        session = DBSession()
        contract = session.query(FutureContract).filter(FutureContract.product == var, FutureContract.exchange.like(loc+'%')).first()
        session.close()
        return contract.to_dict()
    def post(self, var, loc):
        session = DBSession()
        fco = session.query(FutureContract).filter(FutureContract.product == var, FutureContract.exchange.like(loc+'%')).first()
        fcn = FutureContract(**{key: request.form[key] for key in request.form})
        session.delete(fco)
        session.add(fcn)
        session.commit()
        session.close()
        return {'ok': 1}
    def delete(self, var, loc):
        session = DBSession()
        fc = session.query(FutureContract).filter(FutureContract.product == var, FutureContract.exchange.like(loc+'%')).first()
        session.delete(fc)
        session.commit()
        session.close()
        return {'ok':1}

api.add_resource(FcListApi, '/FcList')
api.add_resource(FcApi, '/Fc/<string:loc>/<string:var>')

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


@app.route('/modify', methods=['GET'])
def modify():
    product = request.args['variety']
    exchange = request.args['location']
    session = DBSession()
    modify_fc = session.query(FutureContract).filter(FutureContract.product == product, FutureContract.exchange.like(exchange+'%')).first()
    session.commit()
    context = modify_fc.to_raw_dict()
    session.close()
    return render_template('modify.html', contexts = context)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
