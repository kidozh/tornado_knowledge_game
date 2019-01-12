import sqlite3
import re
from question_orm import Question
from model_utils import *
from sqlalchemy import MetaData

QUESTION_TEXT_PATH = "plain.txt"
TEXT_THRESHOLD = 5

PROBLEM_RE_TEMPLATE = "\d{0,3}(.+？)\s*A(.+)B(.+)C(.+).*（(\w)）"
FOUR_PROBLEM_RE_TEMPLATE = "\d{0,3}(.+？)\s*A(.+)B(.+)C(.+)D(.+).*（(\w)）"

def parse_problem_by_txt(problem_str:str):
    if re.match(FOUR_PROBLEM_RE_TEMPLATE,problem_str):
        matched_group = re.findall(FOUR_PROBLEM_RE_TEMPLATE,problem_str)[0]
        return matched_group[0],matched_group[1:5],matched_group[5]
    elif re.match(PROBLEM_RE_TEMPLATE,problem_str):
        matched_group = re.findall(PROBLEM_RE_TEMPLATE,problem_str)[0]
        return matched_group[0],matched_group[1:4],matched_group[4]
    else:
        return []


with open(QUESTION_TEXT_PATH,'r',encoding='UTF-8') as questionFile:
    question_obj_list = []
    meta = MetaData()
    db_session = getDBSession()
    for line in questionFile:
        if len(line) > TEXT_THRESHOLD:

            res = parse_problem_by_txt(line)
            if res != []:

                question_str, options_list, rightAnswer = res
                saved_question_obj = None
                if len(options_list) == 3:
                    saved_question_obj = Question(question=question_str,
                                                  optionA=options_list[0],
                                                  optionB=options_list[1],
                                                  optionC=options_list[2],
                                                  optionD="",
                                                  rightOption=rightAnswer
                                                  )
                elif len(options_list) == 4:
                    saved_question_obj = Question(question=question_str,
                                                  optionA=options_list[0],
                                                  optionB=options_list[1],
                                                  optionC=options_list[2],
                                                  optionD=options_list[3],
                                                  rightOption=rightAnswer
                                                  )
                else:

                    pass

                question_obj_list.append(saved_question_obj)


            else:
                print(line)
                pass

    db_session.add_all(question_obj_list)
    db_session.commit()
    print("DONE!",len(question_obj_list))
