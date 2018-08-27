from sqlalchemy import Column, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
import json,os

with open(os.path.dirname(os.path.realpath(__file__))+'//map_dict.json', 'r', encoding = 'utf-8') as f:
    map_dict = json.loads(f.read())

# create Base Object
Base = declarative_base()
def to_dict(self):
    """字典的形式返回某个数据库对象
    由于数据库以英文字段存储，此方法将其映射为中文，若不需要映射成中文，用如下的 to_raw_dict 方法
    """

    tmp_dict = {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
    return {map_dict[key]:tmp_dict[key] for key in tmp_dict}

def to_raw_dict(self):
    return{c.name:getattr(self, c.name, None) for c in self.__table__.columns}

Base.to_dict = to_dict
Base.to_raw_dict = to_raw_dict

class FutureContract(Base):
    __tablename__ = 'contract'

    id = Column(Integer, autoincrement = True, primary_key = True)
    product = Column(Text, default = '')
    unit = Column(Text, default = '')
    offer_unit = Column(Text, default = '')
    tick = Column(Text, default = '')
    raising_limit = Column(Text, default = '')
    contract_month = Column(Text, default = '')
    trading_time = Column(Text, default = '')
    last_trading_date = Column(Text, default = '')
    last_delivery_date = Column(Text, default = '')
    delivery_grade = Column(Text, default = '')
    delivery_site = Column(Text, default = '')
    trading_margin = Column(Text, default = '')
    delivery_method = Column(Text, default = '')
    code = Column(Text, default = '')
    exchange = Column(Text, default = '')
    delivery_unit = Column(Text, default = '')
    trading_fee = Column(Text, default = '')
    multiplier = Column(Text, default = '')
    national_debt = Column(Text, default = '')
    offer_method = Column(Text, default = '')
    settlement_currency = Column(Text, default = '')
