# 导入:
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from model_utils import *

Base = declarative_base()



class Question(Base):
    # 表的名字:
    __tablename__ = 'question'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    question = Column(String(50))
    optionA = Column(String(20))
    optionB = Column(String(20))
    optionC = Column(String(20))
    optionD = Column(String(20))
    rightOption = Column(String(20))

if __name__ == "__main__":
    engine = getEngine()
    metadata = MetaData(engine)
    question_table = Table(
        Question.__tablename__,metadata,
        Column("id",Integer, primary_key=True),
        Column("question",String(50)),
        Column("optionA",String(50)),
        Column("optionB",String(50)),
        Column("optionC",String(50)),
        Column("optionD",String(50)),
        Column("rightOption", String(50)),

                           )
    metadata.create_all()


    conn = engine.connect()

