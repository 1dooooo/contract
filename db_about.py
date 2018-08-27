from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from FutureContract import Base
from urllib.parse import quote_plus as urlquote
# engine = create_engine('postgresql://postgres:yisheng@192.168.23.180:5432/postgres')
engine = create_engine('postgresql://root:%s@postgres-gqjljrlw.sql.tencentcdb.com:34160/cspcommodityf10' % urlquote(quote1234!@#$))
DBSession = sessionmaker(bind=engine)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
