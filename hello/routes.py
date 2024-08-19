from flask import render_template,flash,redirect,url_for,request,session
from hello.forms import RegisterForm,LoginForm,ForgotPasswordForm,ResetPasswordForm
from werkzeug.security import generate_password_hash, check_password_hash
from hello.models import User
from hello import app,db,mail
import pandas as pd
from flask_login import current_user,login_manager,login_user
from flask_mail import Message
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from automated_everything import connect_to_croptrak as cc
import os
    
# with app.app_context():
#     db.create_all()  

# data 
UPLOAD_FOLDER = 'UPLOAD_FOLDER'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
df = cc.connect_croptrak()
df_croptrak = cc.show_area_name()
df_area = df_croptrak['Area_Name'].unique()

data = {
    'df':df,
    'df_area': df_area
}
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',title ='Welcome to Walther Farms')

@app.route('/about')
def about():
    if 'user_id' in session:
        # df = ['Table A', 'Table B', 'Table C', 'Table D']
        # Display the DataFrame in the 'about.html' template
        return render_template('about.html', data=data,tables=[df_croptrak.to_html(classes='data',index=False)], titles=df_croptrak.columns.values)
    else:
        # Display a message asking the user to log in
        flash('You need to log in first.', 'danger')
        return render_template('about.html',title="About Page")

@app.route("/register",methods =["POST","GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    # if form.validate_on_submit():
    #     flash(f"Account Created for {form.username.data}!","Sucess!!!")
    #     return redirect(url_for('home'))
    if form.validate_on_submit():
        # Process the form data
        # ...
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Registration successful! for {form.username.data}', 'success')
        return redirect(url_for('login'))
    else:
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{field.title()} field - {error}", 'danger')
                    
    return render_template('register.html',title="Registration",forms = form)

@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            flash(f'You have successfully logged in, {user.username}!', 'success')
            session['user_id'] = user.id
            if form.remember.data:
                session.permanent = True 
            return redirect(url_for('about'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')
            return render_template('login.html', title="Login", forms=form)
    return render_template('login.html', title="Login", forms=form)

def send_reset_mail(user):
    with app.app_context():
        token = user.generate_reset_token(user.id)
        msg = Message("Password Reset Request", sender='noreply@example.com', recipients=[user.email])
        msg.body = f'''
        To Reset Password, Visit the following link:
        {url_for('reset_password', token=token, _external=True)}

        If you did not make this request, simply ignore it.
        '''
        mail.send(msg)

@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_mail(user)
        flash(f"Reset password has been sent to {user.email}","Success")
        return redirect(url_for('login'))
    return render_template('forgot_password.html',title ='forgot password',form= form)




@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('forgot_password'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You can now login', 'success')
        return redirect(url_for('login'))

    return render_template('reset_password.html', title='Reset Password', form=form, token=token)

@app.route('/join_data',methods=["GET", "POST"])
def join_data():
    if request.method == "POST":
        croptrak = request.form.get("croptable")
        agvise = request.form.get("agtable")
        year = request.form.get("yrtable")
        print(year)
        return redirect(url_for('show_data',croptrak = croptrak,agvise = agvise,year=year))
    return render_template('table.html')

@app.route('/show_data/<croptrak><agvise>/<year>',methods=['GET','POST'])
def show_data(croptrak,agvise,year):
    if request.method == "POST":
        file_path = os.path.join(app.config['UPLOAD_FOLDER'],croptrak)
        if croptrak.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif croptrak.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            flash('Unsupported file format')
    
    return render_template('show.html',data = croptrak)
    