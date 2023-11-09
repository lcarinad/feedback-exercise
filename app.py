from flask import Flask, render_template, redirect, session, flash
# from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import UserForm, LoginForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
app.app_context().push()
# toolbar = DebugToolbarExtension(app)

@app.route('/')
def show_home():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = UserForm()
    if form.validate_on_submit(): 
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user) 
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username take. Please pick another name.')
            return render_template("register.html", form = form)
        session['user'] = new_user.username
        flash(f"Welcome {new_user.first_name}! You succesfully Created Your Account!", "success")
        return redirect(f'/users/{new_user.username}')
    
    return render_template("register.html", form = form)

@app.route(f"/users/<username>")
def show_user(username):
    if 'user' not in session:
        flash("Please login first!", "danger")
        return redirect('/')
    else:
        user = User.query.get_or_404(username)
        
    return render_template('user.html', user = user)

@app.route('/login', methods = ['GET', 'POST'])
def login_user():
    form = LoginForm()
    if form.validate_on_submit(): 
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome back, {user.first_name}!", "primary")
            session['user'] = user.username
            
            return redirect(f'/users/{user.username}')
    
    return render_template('login.html', form = form)

@app.route('/logout')
def logout_user():
    session.pop('user')
    flash(f"Goodbye✌🏾", "info")
    return redirect('/')