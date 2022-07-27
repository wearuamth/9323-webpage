from flask import Blueprint,render_template,request,g,redirect,url_for,flash
from decorators import login_required
from .forms import QuestionForm,AnswerForm,CourseForm
from models import QuestionModel,AnswerModel,CourseModel
from exts import db
from sqlalchemy import or_


bp = Blueprint("qa",__name__,url_prefix="/")


@bp.route("/")
def index():
    questions = QuestionModel.query.order_by(db.text("-create_time")).all()
    return render_template("index.html",questions=questions)

@bp.route("/course",methods=['GET','POST'])
def create_course():
    if request.method == 'GET':
        return render_template("course.html")
    else:
        form = CourseForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            course = CourseModel(title=title,content=content,author=g.user)
            db.session.add(course)
            db.session.commit()
            return redirect("/")
        else:
            flash("Wrong Format!")
            return redirect(url_for("qa.public_question"))

@bp.route("/course/add/<int:question_id>",methods=['GET','POST'])
def add_course(question_id):
    if request.method == 'GET':
        return render_template("course.html")
    else:
        lecturer = g.user
        course = CourseModel.query.filter_by(author_id=lecturer.id).first()
        question = QuestionModel.query.get(question_id)
        question.course_id = course.id
        db.session.commit()
        return redirect(f"/question/{question_id}")

@bp.route("/course/del/<int:course_id>",methods=['GET','DELETE'])
def del_course(course_id):
    if request.method == 'GET':
        return render_template("course.html")
    else:
        course = CourseModel.query.filter_by(id == course_id).first()
        db.session.delete(course)
        db.session.commit()
        return redirect("/profile")


@bp.route("/question/public",methods=['GET','POST'])
@login_required
def public_question():
    # 判断是否登录，如果没有登录，跳转到登录页面
    if request.method == 'GET':
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title,content=content,author=g.user,course_id=0)
            db.session.add(question)
            db.session.commit()
            return redirect("/")
        else:
            flash("Wrong Format!")
            return redirect(url_for("qa.public_question"))


@bp.route("/question/<int:question_id>")
@login_required
def question_detail(question_id):
    question = QuestionModel.query.get(question_id)
    answers = AnswerModel.query.filter_by(question_id=question.id).order_by(db.text("-likes")).all()
    return render_template("detail.html", question=question,user=g.user,answers = answers)



@bp.route("/answer/<int:question_id>",methods=['POST'])
@login_required
def answer(question_id):
    user = g.user
    qa = QuestionModel.query.filter_by(id=question_id).first()
    if (user.u_type == 'student' and user.c_id == qa.course_id) or \
       (user.u_type == 'lecturer' and user.id == qa.course.author_id) or \
       (user.u_type == 'organ' and user.id == qa.author_id):
        form = AnswerForm(request.form)
        if form.validate():
            content = form.content.data
            answer_model = AnswerModel(content=content,author=g.user,question_id=question_id,likes=0)
            db.session.add(answer_model)
            db.session.commit()
            return redirect(url_for("qa.question_detail",question_id=question_id))
        else:
            flash("Wrong Format!")
            return redirect(url_for("qa.question_detail", question_id=question_id))
    else:
        if user.u_type == 'student':
            flash("Join this course first!")
        else:
            flash("Join this course as student!")
        return redirect(url_for("qa.question_detail", question_id=question_id))


@bp.route("/search")
def search():
    # /search?q=xxx
    q = request.args.get("q")
    # filter_by：直接使用字段的名称
    # filter：使用模型.字段名称
    questions =QuestionModel.query.filter(or_(QuestionModel.title.contains(q),QuestionModel.content.contains(q))).order_by(db.text("-create_time"))
    return render_template("index.html",questions=questions)

@bp.route("/likes/<int:answer_id>")
def likes(answer_id):
    answer = AnswerModel.query.filter_by(id=answer_id).first()
    answer.likes += 1
    q_id = answer.question_id
    db.session.commit()
    return redirect(url_for("qa.question_detail",question_id = q_id))


