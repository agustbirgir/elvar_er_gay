from flask import Flask, render_template, request, session, redirect, url_for
import pyrebase
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(8)

# tengin við firebase realtime database á firebase.google.com 
config = {
    "apiKey": "AIzaSyAwDhualpMaZvQvIW1oWKr8-s1WiyXNDis",
    "authDomain": "verkefni6-557d2.firebaseapp.com",
    "databaseURL": "https://verkefni6-557d2.firebaseio.com",
    "projectId": "verkefni6-557d2",
    "storageBucket": "verkefni6-557d2.appspot.com",
    "messagingSenderId": "587824470344",
    "appId": "1:587824470344:web:3228b437945dcef45c7b7d",
    "measurementId": "G-B9VJTTSLVP"
}

fb = pyrebase.initialize_app(config)
db = fb.database()

# Test route til að setja gögn í db
@app.route('/')
def index():
    db.child("users").push({"user":"Toto", "pwd":"oz"}) 
    #db.child("bill").push({"nr":"abc12", "tegund":"Ford","utegund":"Mustang","argerd":"2077","akstur":"10000","verd":"5,5m"}) 
    return render_template('index.html')

# Test route til að sækja öll gögn úr db
 

@app.route('/bilasala') 
def secret():
    if 'logged_in' in session:
        b = db.child('bill').get().val()
        lst = list(b.items())
        return render_template('bilasala.html', bilar=lst, user=username)
    else: 
        return redirect('/')

@app.route('/bill/<id>')
def car(id):
    c = db.child('bill').child(id).get().val()
    bill = list(c.items())
    return render_template('car.html', bill=bill, id=id)

@app.route('/skrabil')
def skrabil():
    render_template('nyskrabil.html')

@app.route('/nyskrabil',methods=['POST'])
def nyskra():
    skrnr = []
    if request.method == 'POST':
        nr = request.form['nr']
        tegund = request.form['tegund']
        utegund = request.form['utegund']
        tegund = request.form['tegund']
        argerd = request.form['argerd']
        akstur = request.form['akstur']
        verd = request.form['verd']

        u = db.child('bill').get().val()
        lst = list(u.items())
        for i in lst:
            skrnr.append(i[1]['nr'])
        if nr not in skrnr:
            db.child('bill').push({ 'nr':nr, 'tegund':tegund, 'utegund':utegund, 'argerd':argerd, 'asktur':akstur, 'verd':verd })
            return render_template('nyskraok.html', nr = nr)
        else:
            return render_template('skraningertil.html', nr = nr)

@app.route('/bill/breytaeyda',methods=['POST'])
def breytaeyda():
    if request.method == 'POST':
        if request.form['submit'] == 'eyda':
            db.child('bill').child(request.form['id']).remove()
            return render_template('deleted.html', nr = request.form['nr'])
        else:
            db.child('bill').child(request.form['id']).update({
            'nr':request.form['nr'],
            'tegund':request.form['tegund'],
            'utegund':request.form['utegund'],
            'argerd':request.form['argerd'],
            'akstur':request.form['akstur'],
            'verd':request.form['verd']})
            return render_template('updated.html', nr = request.form['nr'])
    else:
        return render_template('no_method.html')


@app.route('/login', methods=['GET','POST'])
def login():
    login = False
    if request.method == 'POST':
        
        usr = request.form['usrname']
        pwd = request.form['psword']
        
        u = db.child('users').get().val()
        lst = list(u.items())
        global username
        for i in lst:
            if usr == i[1]['user'] and pwd == i[1]['pwd']: #ath! user í db
                login = True
                username = i[1]['user'] #ath! user 
                break
        if login:
            session['logged_in'] = usr
            return redirect('/bilasala')
        else:
            return render_template('nologin.html')
    else:
        return render_template('no_method.html')

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/doregister',methods=['GET','POST'])
def doregister():
    usernames = [] 
    if request.method == 'POST':
        usr = request.form['usrname']
        pwd = request.form['psword']

        u = db.child('users').get().val()
        lst = list(u.items())
        for i in lst:
            usernames.append(i[1]['user'])

        if usr not in usernames:
            db.child('user').push({'usr':usr,'pwd':pwd})
            return render_template("registered.html")
        else:
            return render_template('userexists.html')
    else:
        return render_template('nomethod.html')

            
#Villu leit
@app.errorhandler(404)
def pagenotfound(error):
    return render_template('pagenotfound.html'),404

@app.errorhandler(500)
def servererror(error):
    return render_template('servererror.html'),500

if __name__ == "__main__":
	app.run(debug=True)

# skrifum nýjan í grunn hnútur sem heitir notandi 
# db.child("notandi").push({"notendanafn":"dsg", "lykilorð":1234}) 

# # förum í grunn og sækjum allar raðir ( öll gögn )
# u = db.child("notandi").get().val()
# lst = list(u.items())