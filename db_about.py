from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from FutureContract import Base

engine = create_engine('mysql+mysqlconnector://contract:contract@127.0.0.1:3306/contract')

DBSession = sessionmaker(bind=engine)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
