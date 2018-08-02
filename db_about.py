from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from FutureContract import OutFutureContract
import json


engine = create_engine('postgresql://postgres:yisheng@192.168.23.180:5432/postgres', echo=True)

DBSession = sessionmaker(bind=engine)

if __name__ == '__main__':
    with open('d:/downloads/out_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        session = DBSession()
        for d in data:
            ifc = OutFutureContract(**d)
            session.add(ifc)
        session.commit()