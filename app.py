from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from scraper.scraper import scrape_ayush_data
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

# Flask-Login Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirect to /login if not authenticated

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

# Saved Herb Model
class SavedHerb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["GET"])
@login_required
def search():
    query = request.args.get("query", "").lower()
    results = scrape_ayush_data(query)
    return render_template("search.html", results=results, query=query)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password!")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"], method="pbkdf2:sha256")

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully! Please login.")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/profile")
@login_required
def profile():
    saved_herbs = SavedHerb.query.filter_by(user_id=current_user.id).all()
    return render_template("profile.html", herbs=saved_herbs)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("index"))

# Debugging Session Data
@app.route("/session_check")
def session_check():
    if current_user.is_authenticated:
        return f"Logged in as: {current_user.username}"
    else:
        return "Not authenticated!"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
