from exts import db
from datetime import datetime
# 所有user都可以创建问题
# 老师可以将不属于任何course的proj加入自己的course
# 所有人的搜索界面都是proj，进入proj，会显示是否属于某一个course

class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    captcha = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    o_name = db.Column(db.String(20), nullable=False)
    u_type = db.Column(db.String(10), nullable=False)
    join_time = db.Column(db.DateTime, default=datetime.now)

    c_id = db.Column(db.Integer)




class QuestionModel(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("UserModel", backref="questions")

    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), default=0)
    course = db.relationship("CourseModel", backref="project")

class CourseModel(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("UserModel", backref="course")

#
# class ProjModel(db.Model):
#     __tablename__ = "proj"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(200), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     create_time = db.Column(db.DateTime, default=datetime.now)
#
#     course_id = db.Column(db.Integer, db.ForeignKey("course.id"), default=-1)
#     course = db.relationship("CourseModel", backref="project")
#
#     author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
#     author = db.relationship("UserModel", backref="project")


class AnswerModel(db.Model):
    __tablename__ = "answer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    question = db.relationship("QuestionModel", backref=db.backref("answers", order_by=create_time.desc()))
    author = db.relationship("UserModel", backref="answers")
