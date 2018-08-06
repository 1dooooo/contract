from sqlalchemy import Column, Text
from sqlalchemy.ext.declarative import declarative_base
import json


# create Base Object
Base = declarative_base()
def to_dict(self):
    with open('map_dict.json', 'r', encoding = 'utf-8') as f:
        map_dict = json.loads(f.read())
    tmp_dict = {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
    return {map_dict[key]:tmp_dict[key] for key in tmp_dict}
Base.to_dict = to_dict

class FutureContract(Base):
    __tablename__ = 'contract'

    exchange = Column(Text)
    product = Column(Text,primary_key=True)
    code = Column(Text,primary_key=True)
    unit = Column(Text)
    tick = Column(Text)
    last_trading_date = Column(Text)
    tradingTime = Column(Text)
    night_tradingtime = Column(Text)
    ltd_tradingtime = Column(Text)
    exch_fee = Column(Text)
    margin = Column(Text)
    max_handnum = Column(Text)
    delivery_method = Column(Text)
    exch_delivery_fee = Column(Text)
    delivery_unit = Column(Text)
    delivery_settlemnt_price = Column(Text)
    last_delivery_date = Column(Text)
    position_margin = Column(Text)
    raising_limit_margin1 = Column(Text)
    raising_limit_margin2 = Column(Text)
    dmargin_adjust_date = Column(Text)
    delivery_month_margin = Column(Text)
    raising_limit = Column(Text)
    raising_limit_1 = Column(Text)
    raising_limit_2 = Column(Text)
    position_limit = Column(Text)
    dMonth_position_limit = Column(Text)
    Pre_dmonth_position_limit = Column(Text)
    currency = Column(Text)
    contract_month = Column(Text)
    offer = Column(Text)
    declaration_level = Column(Text)
    first_notice_day = Column(Text)
