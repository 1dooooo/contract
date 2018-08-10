from sqlalchemy import Column, Text
from sqlalchemy.ext.declarative import declarative_base
import json

# create Base Object
Base = declarative_base()
def to_dict(self):
    
    with open('/var/www/contract/map_dict.json', 'r', encoding = 'utf-8') as f:
        map_dict = json.loads(f.read())
    tmp_dict = {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
    return {map_dict[key]:tmp_dict[key] for key in tmp_dict}

def to_raw_dict(self):
    return{c.name:getattr(self, c.name, None) for c in self.__table__.columns}

Base.to_dict = to_dict
Base.to_raw_dict = to_raw_dict

class FutureContract(Base):
    __tablename__ = 'contract'

    exchange = Column(Text, default='')
    product = Column(Text,primary_key=True,default='')
    code = Column(Text,primary_key=True,default='')
    unit = Column(Text, default='')
    tick = Column(Text, default='')
    last_trading_date = Column(Text, default='')
    tradingTime = Column(Text, default='')
    night_tradingtime = Column(Text, default='')
    ltd_tradingtime = Column(Text, default='')
    exch_fee = Column(Text, default='')
    margin = Column(Text, default='')
    max_handnum = Column(Text, default='')
    delivery_method = Column(Text, default='')
    exch_delivery_fee = Column(Text, default='')
    delivery_unit = Column(Text, default='')
    delivery_settlemnt_price = Column(Text, default='')
    last_delivery_date = Column(Text, default='')
    position_margin = Column(Text, default='')
    raising_limit_margin1 = Column(Text, default='')
    raising_limit_margin2 = Column(Text, default='')
    dmargin_adjust_date = Column(Text, default='')
    delivery_month_margin = Column(Text, default='')
    raising_limit = Column(Text, default='')
    raising_limit_1 = Column(Text, default='')
    raising_limit_2 = Column(Text, default='')
    position_limit = Column(Text, default='')
    dMonth_position_limit = Column(Text, default='')
    Pre_dmonth_position_limit = Column(Text, default='')
    currency = Column(Text, default='')
    contract_month = Column(Text, default='')
    offer = Column(Text, default='')
    declaration_level = Column(Text, default='')
    first_notice_day = Column(Text, default='')
