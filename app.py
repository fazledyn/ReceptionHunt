import time
import hashlib

from flask import Flask, request, redirect, url_for
from flask import render_template
from flask_login import UserMixin, LoginManager, login_user, current_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hunt.db'
app.config['SECRET_KEY'] = 'TOR_BAAP_ATAF'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

#####################################################################################
############################# DATABASE MODELS #######################################

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True)
    pwd = db.Column(db.String(80), nullable=False)
    token = db.Column(db.String(10), nullable=False)
    level_completed = db.Column(db.Integer, default=0)
    last_time = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(10), default="TEAM")

    def __repr__(self):
        return "ID: %r" % self.id + " Name: " + self.name + " Pass: " + self.pwd


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(20), unique=True)

    def __repr__(self):
        return "ID: " + str(self.id) + " Answer: " + self.answer


class Answers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, nullable=False)
    team = db.Column(db.String(25), nullable=False)
    answer = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return "Level: " + str(self.level) + " Team: " + self.team + " Answer: " + self.answer


############################# DATABASE MODELS #######################################
#####################################################################################

#####################################################################################
############################## ROUTE HANDLERS #######################################


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("index"))


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html")

    elif request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(name=username).first()
        password = hashlib.sha256(password.encode()).hexdigest()

        if user is not None and password == user.pwd:
            user_is_logged_in = True
            login_user(user)
            return redirect(url_for("puzzle"))
        else:
            return redirect(url_for("index"))

    else:
        return "Backend FUCKED UP badly"


@app.route("/puzzle", methods=['GET', 'POST'])
@login_required
def puzzle():
    TOTAL_QUIZ = len(Quiz.query.all())

    if request.method == 'POST':
        current_level = current_user.level_completed + 1
        print("POST")
        print(current_level)

        if current_level > TOTAL_QUIZ:
            print("POST + CURRENT_LEVEL == TOTAL_QUIZ")
            return redirect(url_for("congrats"))

        else:
            print("POST + ")
            answer = request.form.get("answer")
            answer_lower = answer.lower()
            current_puzzle_no = current_user.token[current_level-1]
            current_puzzle = Quiz.query.filter_by(id=current_puzzle_no).first()

            answer_record = Answers(level=current_level, team=current_user.name, answer=answer)
            db.session.add(answer_record)
            db.session.commit()

            if answer_lower == current_puzzle.answer:
                user = User.query.filter_by(name=current_user.name).first()
                new_level = user.level_completed + 1
                user.last_time = datetime.now()
                user.level_completed = new_level
                db.session.commit()

                user = User.query.filter_by(name=current_user.name).first()
            else:
                user = User.query.filter_by(name=current_user.name).first()

            return redirect(url_for("puzzle"))

    elif request.method == 'GET':

        if current_user.level_completed == TOTAL_QUIZ:
            print("GET + CURRENT_LEVEL == TOTAL_QUIZ")
            return redirect(url_for("congrats"))
        else:
            print("GET ELSE")
            print("Current User Level Completed: ", current_user.level_completed)
            imageFile = "images/" + current_user.token[current_user.level_completed] + ".png"
            image_link = url_for('static', filename=imageFile)
            return render_template("puzzle.html", level=current_user.level_completed+1, image_link=image_link)

    else:
        return "You're not supposed to be here !"


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/congrats")
@login_required
def congrats():
    return render_template("congrats.html")


@app.route("/leaderboard")
@login_required
def leaderboard():
    # ordering the leaderboard by the user standings in a descending order
    user_list = User.query.filter_by(role="TEAM").order_by(User.level_completed.desc(), User.last_time.asc())
    return render_template("leaderboard.html", user_list=user_list)

@login_required
@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if request.method == 'GET':
        return render_template("admin_login.html")

    elif request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        print(username, password)
        if username == "admin" and password == "admin":
            admin_user = User.query.filter_by(name=username).first()
            login_user(admin_user)
            return redirect(url_for("admin_dashboard"))
        else:
            return redirect(url_for("admin"))

    else: 
        return redirect(url_for("index"))

@login_required
@app.route("/team_reg", methods=['GET', 'POST'])
def team_reg():
    if current_user.name == "admin":
        if request.method == 'GET':
            return render_template("team_register.html")

        elif request.method == 'POST':
            teamname = request.form.get("teamname")
            password = request.form.get("password")
            token = request.form.get("token")

            password_hash = hashlib.sha256(password.encode()).hexdigest()
            user = User(name=teamname, pwd=password_hash, token=token)
            db.session.add(user)
            db.session.commit()

            return render_template("team_register.html")
        else:
            return "Backend fucked up badly !"
    else:
        return redirect(url_for("index"))

@login_required
@app.route("/admin_dashboard", methods=['GET', 'POST'])
def admin_dashboard():
    if current_user.name == "admin":

        if request.method == 'GET':
            answer_list = Answers.query.order_by(Answers.level.asc())
            return render_template("answer_page.html", answer_list=answer_list)

        elif request.method == 'POST':
            teamname = request.form.get("teamname")
            level = request.form.get("level")

            if level == "" and teamname != "":
                answer_list = Answers.query.filter_by(team=teamname)
            elif teamname == "" and level != "":
                level_int = int(level)
                answer_list = Answers.query.filter_by(level=level_int)
            elif level != "" and teamname != "":
                level_int = int(level)
                answer_list = Answers.query.filter_by(team=teamname, level=level_int)
            else:
                answer_list = Answers.query.order_by(Answers.level.asc())

            return render_template("answer_page.html", answer_list=answer_list)

        else:
            return "Backend fucked up badly !"
    else:
        return redirect(url_for("index"))
        
############################## ROUTE HANDLERS #######################################
#####################################################################################

if __name__ == "__main__":
    app.run(debug=True)
