from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from FutureContract import Base

engine = create_engine('postgresql://postgres:sun4213@localhost:5432/contract')

DBSession = sessionmaker(bind=engine)

if __name__ == '__main__':
    Base.metadata.create_all(engine)