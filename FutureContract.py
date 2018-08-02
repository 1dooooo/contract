from sqlalchemy import Column, Text
from sqlalchemy.ext.declarative import declarative_base


# create Base Object
InBase = declarative_base()
def to_dict(self):
    map_dict = {"exchange":"交易所", "product":"品种", "code":"代码", "unit":"合约单位", "tick":"最小跳动", "last_trading_date":"最后交易日", "tradingTime":"白盘交易时间", "night_tradingtime":"夜盘交易时间", "ltd_tradingtime":"最后交易日特殊交易时间", "exch_fee":"手续费", "margin":"正常保证金", "max_handnum":"单笔最大下单(手)", "delivery_method":"交割方式", "exch_delivery_fee":"交割费用", "delivery_unit":"交割单位", "delivery_settlemnt_price":"交割结算价", "last_delivery_date":"交割日期", "position_margin":"持仓量变化 保证金", "raising_limit_margin1":"第一板结算起 保证金", "raising_limit_margin2":"第二板结算起 保证金", "dmargin_adjust_date":"临近交割月交易所首次保证金调整(%)", "delivery_month_margin":"交割月保证金", "raising_limit":"正常涨跌幅", "raising_limit_1":"第一板结算起 涨跌幅", "raising_limit_2":"第二板结算起 涨跌幅", "postion_limit":"一般月份单边限仓", "dMonth_position_limit":"交割前月限仓", "Pre_dmonth_position_limit":"交割月限仓"
}
    tmp_dict = {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
    return {map_dict[key]:tmp_dict[key] for key in tmp_dict}
InBase.to_dict = to_dict

OutBase = declarative_base()
def to_dict(self):
    map_dict = {"product":"名称", "code":"品种代码", "exchange":"交易所", "unit":"合约单位", "tick":"最小波动单位", "worth":"最小波动价值", "currency":"结算货币", "contract_month":"合约月份", "tradingTime":"交易时间", "last_trading_date":"最后交易日", "margin":"保证金", "raising_limit":"涨跌幅限制", "delivery_method":"交割方式", "offer":"报价", "declaration_level":"申报水平", "position_limit":"持仓限额", "first_notice_day":"首次通知日"

}
    tmp_dict = {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
    tmp_dict.pop('id')
    return {map_dict[key]:tmp_dict[key] for key in tmp_dict}

OutBase.to_dict = to_dict


class OutFutureContract(OutBase):
    __tablename__ = 'outcontract'

    id = Column(Text)
    product = Column(Text,primary_key=True)
    code = Column(Text)
    exchange = Column(Text)
    unit = Column(Text)
    tick = Column(Text)
    worth = Column(Text)
    currency = Column(Text)
    contract_month = Column(Text)
    tradingTime = Column(Text)
    last_trading_date = Column(Text)
    margin = Column(Text)
    raising_limit = Column(Text)
    delivery_method = Column(Text)
    offer = Column(Text)
    declaration_level = Column(Text)
    position_limit = Column(Text)
    first_notice_day = Column(Text)

class InFutureContract(InBase):
    __tablename__ = 'incontract'

    exchange = Column(Text)
    product = Column(Text,primary_key=True)
    code = Column(Text)
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
    postion_limit = Column(Text)
    dMonth_position_limit = Column(Text)
    Pre_dmonth_position_limit = Column(Text)