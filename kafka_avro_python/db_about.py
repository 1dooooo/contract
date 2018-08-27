from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from FutureContract import Base

engine = create_engine('postgresql://postgres:yisheng@192.168.23.180:5432/postgres')

DBSession = sessionmaker(bind=engine)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
