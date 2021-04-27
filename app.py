from types import SimpleNamespace
from flask import Flask,render_template,abort,request, redirect
from flask.globals import session
from flask.helpers import flash, url_for
from flask.wrappers import Request
import sqlalchemy
from forms import signUpForm, loginForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///PawsRescueCenter.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True,unique=True,nullable=False)
    full_name = db.Column(db.String,nullable=False)
    email = db.Column(db.String,unique=True,nullable=False)
    password = db.Column(db.String,nullable=False)
    pets = db.relationship('Pet',backref='user')

class Pet(db.Model):
    id = db.Column(db.Integer,primary_key=True,unique=True,nullable=False)
    name = db.Column(db.String,unique=True,nullable=False)
    age = db.Column(db.Integer)
    bio = db.Column(db.String(300))
    posted_by = db.Column(db.String,db.ForeignKey('user.id'))
    


db.create_all()

'''
pets = [
            {"id": 1, "name": "Nelly", "age": "5 weeks", "bio": "I am a tiny kitten rescued by the good people at Paws Rescue Center. I love squeaky toys and cuddles."},
            {"id": 2, "name": "Yuki", "age": "8 months", "bio": "I am a handsome gentle-cat. I like to dress up in bow ties."},
            {"id": 3, "name": "Basker", "age": "1 year", "bio": "I love barking. But, I love my friends more."},
            {"id": 4, "name": "Mr. Furrkins", "age": "5 years", "bio": "Probably napping."}, 
        ]

new_pet1 = Pet(name="Nelly",age="5 weeks",bio="I am a tiny kitten rescued by the good people at Paws Rescue Center. I love squeaky toys and cuddles.")
new_pet2 = Pet(name="Yuki",age="8 month",bio="I am a handsome gentle-cat. I like to dress up in bow ties.")
new_pet3 = Pet(name="Basker",age="1 year",bio="I love barking. But, I love my friends more.")
new_pet4 = Pet(name="Mr. Furrkins",age="5 years",bio="Probably napping.")
db.session.add(new_pet1)
db.session.add(new_pet2)
db.session.add(new_pet3)
db.session.add(new_pet4)
try:
    db.session.commit()
except Exception as e: 
    print(e)
    db.session.rollback()
finally:
    db.session.close() '''








@app.route("/login",methods=["GET", "POST"])
def login():
    form=loginForm()   
    if(form.validate_on_submit()):
        user_log = User.query.filter_by(email=form.email.data).filter_by(password=form.password.data).first()
        if(user_log):
            session["user"] = user_log.full_name
            return render_template("login.html",message="Succesfully Logged In");
        else:
            return render_template("login.html",message="Wrong credentials. Please try again.");
    elif form.errors:
        return render_template("login.html",form=form);
    return render_template("login.html",form=form);


@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for("home"));



@app.route("/signup",methods=["GET", "POST"])
def signUp():
    form=signUpForm()   
    if(form.validate_on_submit()):
            user_query = User.query.filter_by(email = form.email.data).first()
            if not user_query:
                new_user = User(full_name=form.fullName.data ,email= form.email.data,password=form.password.data)
                db.session.add(new_user)
                try:
                    db.session.commit()
                except Exception as e: 
                    db.session.rollback()
                finally:
                    db.session.close()
                return render_template("signup.html",message="User Successfully Created");
            elif user_query:
                return render_template("signup.html",message="This email already exists in the system! Please log in instead.");
    elif form.errors:
        return render_template("signup.html",form=form);
    return render_template("signup.html",form=form);


@app.route('/')
def home():
    all_pets=Pet.query.all()
    return render_template("home.html",pets=all_pets);

@app.route('/about')
def about():
    return render_template("about.html");


@app.route('/details/<int:id>')
def details(id):
    pet = Pet.query.get(id) 
    if pet is None: 
        abort(404, description="No Pet was Found with the given ID")
    return render_template("details.html", pet = pet)
     






if __name__ == "__main__":
    app.run(debug=True)

