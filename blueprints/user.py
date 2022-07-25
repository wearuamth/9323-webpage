from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    session,
    flash,
    g
)
from exts import mail, db
from flask_mail import Message
from models import EmailCaptchaModel, UserModel
import string
import random
from datetime import datetime
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect("/")
            else:
                flash("Wrong Password")
                return redirect(url_for("user.login"))
        else:
            flash("Wrong Format for Email or Password")
            return redirect(url_for("user.login"))


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            o_name = form.o_name.data
            u_type = form.u_type.data
            # md5("zhiliao") = sdafsdfasfsdfsda
            hash_password = generate_password_hash(password)
            user = UserModel(email=email, username=username, password=hash_password,
                             o_name=o_name,u_type=u_type,c_id=0)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user.login"))
        else:
            return redirect(url_for("user.register"))

@bp.route("/logout")
def logout():
    # 清除session中所有的数据
    session.clear()
    return redirect(url_for('user.login'))


# memcached/redis/数据库中
@bp.route("/captcha", methods=['POST'])
def get_captcha():
    # GET,POST
    email = request.form.get("email")
    letters = string.ascii_letters + string.digits
    captcha = "".join(random.sample(letters, 4))
    if email:
        message = Message(
            subject="Answer Verification code",
            recipients=[email],
            body=f"【Answer】Your verification code is:{captcha}, do not share it!"
        )
        mail.send(message)
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if captcha_model:
            captcha_model.captcha = captcha
            captcha_model.create_time = datetime.now()
            db.session.commit()
        else:
            captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()
        print("captcha:", captcha)
        # code: 200，成功的、正常的请求
        return jsonify({"code": 200})
    else:
        # code：400，客户端错误
        return jsonify({"code": 400, "message": "Input Email first"})


@bp.route("/profile", methods=["GET"])
def profile():
    if request.method == "GET":
        user = g.user
        return render_template("profile.html",user=UserModel.query.get(user.id))

@bp.route("/join/<int:course_id>,<int:question_id>",methods=["POST"])
def join_course(question_id,course_id):
    user = UserModel.query.filter_by(id=g.user.id).first()
    user.c_id = course_id
    db.session.commit()
    return redirect(url_for("qa.question_detail", question_id=question_id))

@bp.route("/drop/<int:question_id>",methods=["POST"])
def drop_course(question_id):
    user = UserModel.query.filter_by(id=g.user.id).first()
    user.c_id = 0
    db.session.commit()
    return redirect(url_for("qa.question_detail", question_id=question_id))

