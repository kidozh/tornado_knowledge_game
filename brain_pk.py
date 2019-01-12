import tornado.ioloop
import tornado.web
import tornado.websocket
import os
from model_utils import *
from question_orm import Question
from sqlalchemy.sql.expression import func
import json

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class HostHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        self.render("brain_pk/host.html")

class competitorHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        print(args[0])
        self.render("brain_pk/competitor.html",teamname=args[0])

class SWebSocketHandler(tornado.websocket.WebSocketHandler):

    team_map = {

    }

    host = None

    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        state_dict = json.loads(message)
        print(message)
        problem_info = {
            "state":state_dict

        }
        if state_dict["aim"] == "request_new_problem":
            SWebSocketHandler.host = self
            db_session = getDBSession()
            random_problem = db_session.query(Question).order_by(func.random()).limit(1).all()[0]
            problem_info["problem_str"] = random_problem.question
            options = []
            for i in ["A","B","C"]:
                options.append(getattr(random_problem,"option"+i))
            try:
                if len(random_problem.optionD) != 0:
                    options.append(random_problem.optionD)
            except:
                pass
            problem_info["options"] = options
            problem_info["right_answer"] = random_problem.rightOption
            problem_info["aim"] = state_dict["aim"]

            print(problem_info)
            self.write_message(json.dumps(problem_info))
            if not ("A" in self.team_map and "B" in self.team_map):
                print("TeamNumber is not enough :",self.team_map.keys())
                return
            for waiter in [self.team_map["A"],self.team_map["B"]]:
                try:
                    options = []
                    for i in ["A", "B", "C"]:
                        answer = getattr(random_problem, "option" + i)
                        options.append({"text":answer,"index":i})
                    try:
                        if len(random_problem.optionD) != 0:
                            options.append({"text":random_problem.optionD,"index":"D"})
                        else:
                            options.append({"text": "我放弃", "index": "D"})
                    except Exception as e:
                        print(e)
                        options.append({"text": "我放弃", "index": "D"})
                    problem_info["options"] = options
                    waiter.write_message(json.dumps(problem_info))
                except:
                    print("Lose connect with ..."+waiter)
        elif state_dict["aim"] == "register":
            # handle with register
            teamname = state_dict["teamname"]
            SWebSocketHandler.team_map[teamname] = self
            message_info = {
                "msg":"注册成功! 你当前是"+teamname,
                "teamname":teamname,
                "state": state_dict
            }
            print("Register ",teamname)
            self.write_message(message_info)
        elif state_dict["aim"] == "send_score":
            print(message)
            teamname = state_dict["teamname"]
            if self.host != None:
                self.host.write_message(message)
                message_info = {
                    "msg": "发送至服务器" + teamname,
                    "teamname": teamname,
                    "state": state_dict,
                    "status":0
                }
                self.write_message(message_info)
            else:
                message_info = {
                    "msg": "发送至服务器失败！请联系kidozh",
                    "teamname": teamname,
                    "state": state_dict,
                    "status": 1
                }
                self.write_message(message_info)


    def on_close(self):
        print("WebSocket closed")

    def check_origin(self, origin):
        return True

def make_app():
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "template_path": os.path.join(os.path.dirname(__file__), "template"),
        "cookie_secret": "HHHHDHSdadasasddadadds",
        "xsrf_cookies": True,

    }

    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/host", HostHandler),
        (r"/websocket", SWebSocketHandler),
        (r"/team/(\w+)",competitorHandler)

    ],**settings)

if __name__ == "__main__":


    app = make_app()
    app.listen(8888,)
    tornado.ioloop.IOLoop.current().start()