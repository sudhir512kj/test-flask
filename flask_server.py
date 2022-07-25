from datetime import datetime
from flask_mail import Mail, Message
from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:///C:\\Users\\sures\\test-flask\\tmp\\test.db"
db = SQLAlchemy(app)
mail = Mail(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.username


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    category = db.relationship("Category", backref=db.backref("posts", lazy=True))

    def __repr__(self):
        return "<Post %r>" % self.title


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "<Category %r>" % self.name


@app.route("/mail")
def email():
    msg = Message("Hello Message", sender="admin@test.com", recipients=["to@test.com"])
    mail.send(msg)
    return {}


@app.route("/")
def hello():
    return "Hello, World!"


# ?var=1234
@app.route("/queries")
def getQueries():
    val = request.args.get("var")
    return "Hello, World! {}".format(val)


# user agent details
@app.route("/user-agent")
def userAgent():
    val = request.args.get("var")
    user_agent = request.headers.get("User-Agent")

    response = """
    &lt;p&gt;
    Hello, World! {}
    &lt;br/&gt;
    You are accessing this app with {}
    &lt;/p&gt;
    """.format(
        val, user_agent
    )
    return response


@app.route("/blog/post/<string:post_id>")
def get_post_id(post_id):
    return post_id


@app.route("/use_session")
def use_session():
    if "song" not in session:
        session["songs"] = {"title": "Tapestry", "singer": "Bruno Major"}

    return session.get("songs")


@app.route("/delete_session")
def delete_session():
    session.pop("song", None)
    return "removed song from session"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
