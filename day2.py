from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

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
    """adds new users to the list"""
    if request.method == 'GET':
        return render_template('new_user.html')
    else:
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        id = 0
        for user in local_users:
            id = max(id, user['id'])
        local_users.append({'id':id+1,'name':name,'username':username,'email':email})
        return 'successfully added'
