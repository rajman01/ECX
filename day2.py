from flask import Flask, jsonify, render_template, request, session, redirect, url_for
import requests
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.secret_key='ecxday3'
cluster = MongoClient("mongodb+srv://alameen:8023563906@cluster0-axhwj.mongodb.net/ecx?retryWrites=true&w=majority")
db = cluster['ecx']
collection = db['users']
id = 200
res = requests.get('http://jsonplaceholder.typicode.com/users')
web_users = res.json()
local_users = []
for user in web_users:
    local_users.append({'id': user['id'], 'name': user['name'], 'username': user['username']
                           , 'email': user['email']})
@app.route('/')
def index():
    """index page"""
    return 'Day 2, Simple User API'

@app.route('/users')
def users():
    """ returns an array af all users"""
    return jsonify(local_users)


@app.route('/<string:info>')
def user_info(info):
    """ returns users about a given info"""
    check = []
    for user in local_users:
        for detail in user:
            if user[detail] == info:
                check.append(user)
    if not check:
        return jsonify({"error": "user not found"})
    else:
        return jsonify(check)


@app.route('/delete')
def delete():
    """delete last object in the list"""
    local_users.pop()
    return 'last object deleted'


@app.route('/deleteall')
def deleteall():
    """ delete all object in the list"""
    local_users.clear()
    return 'all object deleted'


@app.route('/newuser',methods=['GET','POST'])
def newuser():
    global id
    """adds new users to the list"""
    if request.method == 'GET':
        return render_template('new_user.html')
    else:
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        local_users.append({'id': id, 'name': name,'username': username, 'email': email})
        id = id + 1
        return redirect(url_for('popopulate'))


@app.route('/popopulate')
def popopulate():
    for user in local_users:
        post = {'_id': user['id'], 'name': user['name'], 'username': user['username'], 'email': user['email']}
        data = collection.find_one(post)
        if not data:
            collection.insert_one(post)
    return 'successfully added to database'


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        if 'user_id' in session:
                return redirect(url_for('status'))
        return render_template('login.html')
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        data = collection.find_one({'username': username, 'email': email})
        if data:
            session['user_id'] = data['_id']
            return redirect(url_for('status'))
        else:
            return redirect(url_for('newuser'))


@app.route('/status')
def status():
    if 'user_id' in session:
        return jsonify({"Message": "you are logged in"})
    else:
        return jsonify({"Message": "please login"})
