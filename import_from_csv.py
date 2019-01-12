from question_orm import Question
from model_utils import *
from sqlalchemy import MetaData
import pandas as pd
import numpy as np

meta = MetaData()
db_session = getDBSession()

data = pd.read_csv("problem.csv")

# print(data)
question_obj_list = []
for index,row in data.iterrows():

    question_str = "[%s] %s " %(row["类型"],row["题目"])
    print(index,row["C"])
    if row["C"] in [np.nan,"nan",""]:
        print("Escape",row["题目"],row["A"],row["B"],row["C"],row["D"])
        continue
    options_list = []
    for i in ["A","B","C","D"]:
        if row[i]:
            options_list.append(row[i])
        else:
            options_list.append("")
    rightAnswer = row["答案"]
    saved_question_obj = Question(question=question_str,
                                  optionA=options_list[0],
                                  optionB=options_list[1],
                                  optionC=options_list[2],
                                  optionD=options_list[3],
                                  rightOption=rightAnswer
                                  )
    question_obj_list.append(saved_question_obj)

db_session.add_all(question_obj_list)
db_session.commit()
print("DONE!",len(question_obj_list))
