import os
from flask import Flask, render_template, request, flash
import smtplib
from re import match

app = Flask(__name__)
app.secret_key = 'ecx-day6'
@app.route('/')
def index():
    return '<h1>Day 6: Mail monkey</h1>'

def validEmail(email):
    return match(r'[\w-]{1,20}@\w{2,20}\.\w{2,3}$',email)

@app.route('/email', methods=['GET','POST'])
def email():
    if request.method == 'GET':
        return render_template('email.html',)
    else:
        to = request.form.get('to')
        subject = request.form.get('subject')
        body = request.form.get('body')
        if not validEmail(to):
            flash(f'Make sure your enter a valid email address', 'danger')
            return render_template('email.html')
        message = 'Subject: {}\n\n{}'.format(subject,body)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('alameenraji31@gmail.com','8034023989')
        server.sendmail('alameenraji31@gmail.com', to, message)
        server.quit()
        flash(f'Message sent successfully', 'success')
        return render_template('email.html')



