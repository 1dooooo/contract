from flask import Flask, render_template, request
from urllib import parse

import collections, json, csv, os

from FutureContract import FutureContract, map_dict
from db_about import DBSession


app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    """批量（文件）上传功能实现及页面渲染
    以 GET 方法请求时，返回 “unpload.html”
    以 POST 方法请求时，处理上传的文件，按照 csv或json 格式解析后添加到数据库
    ----------
    如果文件中存在不符合要求（缺少或多余字段）记录，会导致插入失败，即不会插入任何数据
    ----------
    """
    if request.method == 'POST':
        for file in request.files:
            f = request.files[file]
            #以所上传文件的最右侧 '.' 为分隔符进行分割，得到文件后缀 'post_fix'
            post_fix = f.filename.rsplit('.', 1)[1]
            #将文件的内容读入 'data' 中， 'data' 为 python dict 类型
            #若为csv文件，先临时保存，后读取，删除
            if post_fix == 'csv':
                f.save(os.path.dirname(os.path.realpath(__file__))+"/" + f.filename)
                with open(os.path.dirname(os.path.realpath(__file__))+"/" + f.filename, 'r', encoding = 'utf-8') as file:
                    data = csv.DictReader(file)
                    data = [dict(d) for d in data]
                os.remove(os.path.dirname(os.path.realpath(__file__))+"/"+f.filename)

            #若为 json 类型，直接加载到 'data' 中
            if post_fix == 'json':
                data = json.load(f)
            #构建一个数据库 session
            session = DBSession()
            #从 'data' 构建 FutureContract 对象，并加入数据库
            for d in data:
                fc = FutureContract(**d)
                session.add(fc)
            session.commit()
            session.close()

    return render_template('upload.html')

@app.route('/admin/<int:id>', methods = ['GET'])
@app.route('/admin', methods = ['GET'])
@app.route('/show/<int:id>', methods = ['GET'])
@app.route('/show', methods = ['GET'])
def show(id = None):
    """数据显示及操作（管理员模式）功能及页面渲染
    以 '/show' 请求时，渲染出出所有记录
    以 '/admin' 请求时，会在每条记录后额外渲染出 'modify'和'delete' 按钮
    """
    #以查询字符串请求时，返回具体合约
    if id:
        contracts = DBSession().query(FutureContract).filter(FutureContract.id == id).first().to_dict()
        return render_template('contract.html', contracts = contracts)
    #否则，返回所有记录
    context = collections.defaultdict(list)
    fcs = DBSession().query(FutureContract.id, FutureContract.exchange, FutureContract.product).all()
    for fc in fcs:
        context[fc.exchange].append((fc.id, fc.product))
    return render_template(request.path + '.html', context = context)


@app.route('/add', methods=['POST', 'GET'])
def add():
    """单条记录上传功能及页面
    以 GET 方式：返回上传页面
    以 POST 方式：添加记录到数据库
    """
    if request.method == 'POST':
        fc = FutureContract(**{key: request.form[key] for key in request.form})
        session = DBSession()
        session.add(fc)
        session.commit()
        session.close()
    return render_template('add.html', map_dict = map_dict)

@app.route('/search', methods=['POST'])
def search():
    """搜索功能
    以 SQL 模糊搜索模式查找出所有符合的品种。
    ----------
    没有搜索交易所，只搜索品种
    ----------
    """
    fcs = collections.defaultdict(list)
    keyword = request.form['keyword']
    for fc in DBSession().query(FutureContract.id, FutureContract.exchange, FutureContract.product).filter(FutureContract.product.like("%"+keyword+"%")).all():
        fcs[fc[1]].append({'id': fc[0], 'product': fc[2]})
    return json.dumps(fcs)


@app.route('/delete', methods=['POST'])
def delete():
    """删除功能
    """
    #查询数据并删除
    session = DBSession()
    fc = session.query(FutureContract).filter(FutureContract.id == request.form['data']).first()
    session.delete(fc)
    session.commit()
    session.close()
    return json.dumps({'OK':1})

@app.route('/modify/<int:id>', methods=['GET'])
def modify(id):
    """数据修改页面渲染
    """
    #全局保存以供更新
    global modify_fc
    session = DBSession()
    modify_fc = session.query(FutureContract).filter(FutureContract.id == id).first()
    session.commit()
    context = modify_fc.to_raw_dict()
    session.close()
    #根据所查数据渲染页面
    return render_template('modify.html', context = context, map_dict = map_dict)

@app.route('/update', methods=['POST'])
def update():
    """更新数据功能实现
    """
    fc = FutureContract(**{key: request.form[key] for key in request.form})
    fc.id = modify_fc.id
    session = DBSession()
    #首先删除已保存的记录
    session.delete(modify_fc)
    #添加新纪录
    session.add(fc)
    session.commit()
    session.close()
    return json.dumps({'OK':1})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
