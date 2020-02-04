from flask import Flask, request, redirect, url_for
from flask import render_template
from flask_login import UserMixin, LoginManager, login_user, current_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'TOR_BAAP_ATAF'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True)
    pwd = db.Column(db.String(80), nullable=False)
    level_completed = db.Column(db.Integer, default=0)
    time_completed = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "ID: %r" %self.id + " Name: " + self.name + " Pass: " + self.pwd


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file_name = db.Column(db.String(30), unique=True)
    answer = db.Column(db.String(20), unique=True)

    def __repr__(self):
        return "Filename: " + self.image_file_name + " Answer: " + self.answer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html")
        
    elif request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        print(username + "|" + password)

        user = User.query.filter_by(name=username).first()

        if user is not None and password == user.pwd:
            user_is_logged_in = True
            login_user(user)
        #    return render_template("puzzle.html", level=user.level_completed+1)
            return redirect(url_for("puzzle"))
        else:
            return "Enter correct username or password"

    else:
        return "Backend FUCKED UP badly"


@app.route("/puzzle", methods=['GET', 'POST'])
@login_required
def puzzle():
    if request.method == 'POST':
        current_level = current_user.level_completed + 1

        if current_level >= 8:
            return redirect(url_for("congrats"))
        else:
            print(current_level)

            answer = request.form.get("answer")
            current_puzzle = Quiz.query.filter_by(id=current_level).first()

            print(answer)
            if answer == current_puzzle.answer:
                print(current_user)
                user = User.query.filter_by(name=current_user.name).first()
                new_level = user.level_completed + 1
                user.level_completed = new_level
                db.session.commit()

                user = User.query.filter_by(name=current_user.name).first()
            else:
                user = User.query.filter_by(name=current_user.name).first()

            imageFile = "images/" + str(current_user.level_completed + 1) + ".JPG"
            image_link = url_for('static', filename=imageFile)
            print(image_link)
            return render_template("puzzle.html", level=current_user.level_completed+1, image_link=image_link)

    elif request.method == 'GET':
        if current_user.level_completed >= 8:
            return redirect(url_for("congrats"))
        else:
            imageFile = "images/" + str(current_user.level_completed + 1) + ".JPG"
            image_link = url_for('static', filename=imageFile)
            print(image_link)
            return render_template("puzzle.html", level=current_user.level_completed+1, image_link=image_link)
        
    else:
        return "You're not supposed to be here !"

@app.route("/logout")
@login_required
def logout():
    user_is_logged_in = False
    logout_user()
    return "you're logged out"


@app.route("/congrats")
@login_required
def congrats():
    time = "THIS_IS_TIME_STAMP"
    return render_template("congrats.html", finish_time=time)


@app.route("/dashboard")
@login_required
def dashboard():
    # ordering the leaderboard by the user standings in a descending order
    user_list = User.query.order_by(User.level_completed.desc())
    return render_template("dashboard.html", user_list=user_list)


if __name__ == "__main__":
    app.run(debug=True)