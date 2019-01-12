from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker

def getDBSession():
    # 初始化数据库连接:
    engine = create_engine(getEngineURL(),echo = True)
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)
    DBSession.configure(bind=engine)
    return DBSession()

def getEngine():
    engine = create_engine(getEngineURL())
    return engine

def getEngineURL():
    return 'sqlite:///question.db'