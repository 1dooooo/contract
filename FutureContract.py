from sqlalchemy import Column,String
from sqlalchemy.ext.declarative import declarative_base
import json

# create Base Object
Base = declarative_base()
def to_dict(self):
    
    with open('/www/wwwroot/idooooo.tk/contract/map_dict.json', 'r', encoding = 'utf-8') as f:
        map_dict = json.loads(f.read())
    tmp_dict = {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
    return {map_dict[key]:tmp_dict[key] for key in tmp_dict}

def to_raw_dict(self):
    return{c.name:getattr(self, c.name, None) for c in self.__table__.columns}

Base.to_dict = to_dict
Base.to_raw_dict = to_raw_dict

class FutureContract(Base):
    __tablename__ = 'contract'

    exchange = Column(String(300), default='')
    product = Column(String(50),primary_key=True,default='')
    code = Column(String(50),primary_key=True,default='')
    unit = Column(String(300), default='')
    tick = Column(String(300), default='')
    last_trading_date = Column(String(300), default='')
    tradingTime = Column(String(300), default='')
    night_tradingtime = Column(String(300), default='')
    ltd_tradingtime = Column(String(300), default='')
    exch_fee = Column(String(300), default='')
    margin = Column(String(300), default='')
    max_handnum = Column(String(300), default='')
    delivery_method = Column(String(300), default='')
    exch_delivery_fee = Column(String(300), default='')
    delivery_unit = Column(String(300), default='')
    delivery_settlemnt_price = Column(String(300), default='')
    last_delivery_date = Column(String(300), default='')
    position_margin = Column(String(300), default='')
    raising_limit_margin1 = Column(String(300), default='')
    raising_limit_margin2 = Column(String(300), default='')
    dmargin_adjust_date = Column(String(300), default='')
    delivery_month_margin = Column(String(300), default='')
    raising_limit = Column(String(300), default='')
    raising_limit_1 = Column(String(300), default='')
    raising_limit_2 = Column(String(300), default='')
    position_limit = Column(String(300), default='')
    dMonth_position_limit = Column(String(300), default='')
    Pre_dmonth_position_limit = Column(String(300), default='')
    currency = Column(String(300), default='')
    contract_month = Column(String(300), default='')
    offer = Column(String(300), default='')
    declaration_level = Column(String(300), default='')
    first_notice_day = Column(String(300), default='')
