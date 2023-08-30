from app import app, db
from flask import render_template, redirect, url_for, flash, request
from app.forms import SignUpForm
from app.models import User
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')


# @app.route('/logout', methods = ['GET', 'POST'])
# def logout():
#     logout_user()
#     flash("You have successfully logged out", "success")
#     return redirect(url_for('index'))