from sacco import app
from flask import render_template, redirect, url_for, flash, request
from sacco.models import User, Contributions
from sacco.forms import RegisterForm, LoginForm
from sacco import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    return  render_template('home.html')

@app.route('/contributions', methods=['GET', 'POST'])
@login_required
def contributions_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    #if request.method == "POST":

    if request.method == "GET":
        contributions = Contributions.query.all()
        return render_template('contributions.html', purchase_form=purchase_form, contributions=contributions, selling_form=selling_form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(fname=form.fname.data,
                              lname=form.lname.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()

        #login_user(user_to_create)
        #flash(f'Account created successfully! You are logged in as: {user_to_create.username}', category='success')
        flash(f'Account created request sent successfully! You will be notified once the Administrator Reviews the Details you have submitted.', category='success')

        return redirect(url_for('home_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'{err_msg}')
            print(err_msg)
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():

        attempted_user = User.query.filter_by(email_address=form.email_address.data).first()
        print(attempted_user.approved)
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            
            if attempted_user.approved:
                login_user(attempted_user)
                flash(f'Success! You are logged in as: {attempted_user.email_address}', category='success')
                return redirect(url_for('home_page'))
            else:
                flash(f'Your Account is still under review. You will be notified once the review is complete', category='success')
                return redirect(url_for('home_page'))
        else:
            flash("Email or Password Incorrect!")


    return render_template('login.html', form=form)



@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out', category='info')
    return redirect(url_for('home_page'))

@app.route('/services')
def services_page():
    return render_template('services.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/contact')
def contact_page():
    return render_template('contact.html')