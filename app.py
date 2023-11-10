from flask import Flask, render_template, redirect, session, flash, url_for
# from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import UserForm, LoginForm, FeedbackForm
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

@app.route("/users/<username>")
def show_user(username):
    if 'user' not in session:
        flash("Please login first!", "danger")
        return redirect('/')
    else:
        user = User.query.get_or_404(username)
        feedback = Feedback.query.filter(Feedback.username == session['user'])
        return render_template('user.html', user = user, feedback = feedback)

@app.route("/feedback", methods=['POST', 'GET'])
def submit_feedbackform():
    if "user" not in session:
        flash('Please login first!', "danger")
        return redirect('/register')

    user = User.query.filter_by(username=session['user']).first()
    form = FeedbackForm()
       
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_feedback = Feedback(title = title, content = content, user = user)
        db.session.add(new_feedback)
        db.session.commit()
        flash ("Feedback created!", "success")
        return redirect(url_for('show_user', username=user.username))
    return render_template('feedback.html', form = form, user= user)
        

@app.route("/feedback/<int:id>/edit", methods=['GET', 'POST'])
def edit_feedback(id):
    if "user" not in session:
        flash('Please login first!', "danger")
        return redirect('/register')
    feedback = Feedback.query.get_or_404(id)
    user = feedback.user
    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit(): 
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        flash("You updated your feedback!", "success")
        return redirect(url_for('show_user', username=user.username))
    
    return render_template('feedback_edit_form.html', user = user, feedback = feedback, form = form)

@app.route("/feedback/<int:id>/delete", methods=['GET','POST'])
def delete_feedback(id):
    if "user" not in session:
        flash('Please login first!', "danger")
        return redirect('/register')
    
    feedback = Feedback.query.get_or_404(id)
    user = feedback.user
    if user.username == session['user']:
        db.session.delete(feedback)
        db.session.commit()
        flash("You deleted your feedback!", "warning")
        return redirect(f"/users/{user.username}")

@app.route('/logout')
def logout_user():
    session.pop('user')
    flash(f"Goodbye✌🏾", "info")
    return redirect('/')