from flask import Flask, request, render_template, url_for, redirect, session,jsonify
#from flask_login import login_required,current_user
#from flask.ext.login import LoginManager,login_user
#import mysqlclient

from flask_mysqldb import MySQL
import _mysql_connector
import mysql.connector
import MySQLdb
import MySQLdb.cursors
import re
import io
#import Flask-Mail
# from application import profileName, uploadPicture, profilePicture, allowed_file
from werkzeug.utils import secure_filename
import os
import base64
#from PIL import Image
import io
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import config
import zipfile39
from distutils.log import debug
#import keras
#from keras.preprocessing import image
#import numpy1 as np
#import pickle

### WSGI Application
app = Flask(__name__, template_folder='templates', static_folder='static')

# UPLOAD_FOLDER = 'ProjectCodeSharingSystem\files'

#setting
app.secret_key='sourcecodesharing'
app.config['UPLOAD_FOLDER'] = 'C:\\Users\\Asus\\PycharmProjects\\ProjectCodeSharingSystem\\static'
app.config['MAX_CONTENT_PATH'] = 24 * 1024 * 1024  # max filesize 10mb
#login_manager = LoginManager(app)

# Configure db
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'mysqlcodesharing'
# app.config['MYSQL_PASSWORD'] = 'Mysqlsiva26%'
# app.config['MYSQL_PORT'] = '3306'
# app.config['MYSQL_DB'] = 'code_sharing_system'
#mysql = MySQL(app)
#mysql = mysql.connection
mysql = MySQLdb.connect(user="mysqlcodesharing", host="localhost", password="Mysqlsiva26%", database="code_sharing_system")
#set FLASK ENV=production


# app = Flask(__name__)
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = "username@gmail.com"
# app.config['MAIL_PASSWORD'] = "password"
# mail = Mail(app)
#
# from threading import Thread
#
# def send_email(app, msg):
#     with app.app_context():
#         mail.send(msg)
# msg = Message()
# msg.subject = "Email Subject"
# msg.recipients = ['recipient@gmail.com']
# msg.sender = 'username@gmail.com'
# msg.body = 'Email body'
# Thread(target=send_email, args=(app, msg)).start()
#
#
# def verify_reset_token(token):
#     try:
#         username = jwt.decode(token,
#                               key=os.getenv('SECRET_KEY_FLASK'))['reset_password']
#     except Exception as e:
#         print(e)
#         return
#     return User.query.filter_by(username=username).first()


@app.route("/")
def homepage():
    msg=''
    ip_addr = request.environ['REMOTE_ADDR']
    msg = ' Your IP address is:' + ip_addr
    return  render_template("homepage.html",msg=msg)

@app.route("/index.html")
def index():
   return  render_template("index.html")

@app.route("/login.html",methods=['GET','POST'])
def login():
    ms = ''
    if request.method == 'POST' and 'emailid' in request.form and 'passwords' in request.form:
        emailid = request.form['emailid']
        passwords = request.form['passwords']
        cur = mysql.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM usermast WHERE emailid = % s AND passwords = % s', (emailid, passwords,))
        usermast = cur.fetchone()
        if usermast:
            session['loggedin'] = True
            session['id'] = usermast['id']
            session['emailid'] = usermast['emailid']
            ms = "Logged in successfully !"

            return render_template('profile.html',ms=ms,usermast=usermast)

        else:
            ms = 'Incorrect Email ID / Password !'
    return render_template('login.html', ms=ms)



@app.route("/signup.html",methods=['GET','POST'])
def signup():
    ms=''
    if request.method == 'POST':
             #Fetch form data
        name =  request.form['name']
        lastname =  request.form['lastname']
        emailid =  request.form['emailid']
        passwords =  request.form['passwords']
        confirmpassword =  request.form['confirmpassword']

        if passwords != confirmpassword:
            flash('passwords don\'t match')

        cur = mysql.cursor()
        cur.execute("INSERT INTO usermast(name, lastname, emailid, passwords, confirmpassword) VALUES(%s, %s, %s, %s, %s)",(name, lastname, emailid, passwords, confirmpassword))
        mysql.commit()
        cur = mysql.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM usermast WHERE emailid = % s AND passwords = % s', (emailid, passwords,))
        usermast = cur.fetchone()


        ms = "Sign Up in successfully !"
        return render_template("profile.html",ms=ms,usermast=usermast)

        #   if result>0:
        #      cur = mysql.cursor(MySQLdb.cursors.DictCursor)
        #     cur.execute('SELECT name,emailid FROM usermast WHERE name = %s', (name))
        #    user = cur.fetchone()
    return render_template("signup.html")


@app.route("/profile.html",methods=['GET','POST'])
def profile():
    ms=''
    msg=''
    photo=''
    img=''
    name=''
    if 'loggedin' in session:
        #if request.method == 'POST':
        #     cur = mysql.cursor(MySQLdb.cursors.DictCursor)
        #     cur.execute('SELECT * FROM usermast WHERE emailid = % s ', (session['emailid'],))
        #     usermast = cur.fetchone()
        #     return render_template("profile.html",ms=ms,usermast=usermast)
        #         #myprojects = redirect url_for{{('myproject.html')}},

        # if request.method == 'POST' and 'job' in request.form  and 'pointsremember' in request.form:
        #     job = request.form['job']
        #     pointsremember = request.form['pointsremember']
        #     ms = 'Updated successfully'
        #     cur = mysql.cursor(MySQLdb.cursors.DictCursor)
        #     cur.execute("UPDATE usermast SET  job = %s, pointsremember = %s WHERE emailid = %s", (job, pointsremember, (session['emailid'],)))
        #     mysql.commit()
        #     cur.close()
        #     curs = mysql.cursor(MySQLdb.cursors.DictCursor)
        #     curs.execute('SELECT * FROM usermast WHERE emailid = % s ', (session['emailid'],))
        #     usermast = curs.fetchone()
        #
        #     return render_template("profile.html",ms=ms,usermast=usermast)
        #
         if request.method == 'POST' and 'image' in request.files and 'job' in request.form and 'pointsremember' in request.form:
            image = request.files['image']
            job = request.form['job']
            pointsremember = request.form['pointsremember']

            # id=session['id']
            cur = mysql.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT name FROM usermast WHERE emailid = %s",
                        ((session['emailid'],)))
            name = cur.fetchone()
            cur.close()
            # def convertToBinaryData(filename):
            # Convert digital data to binary format
            # with open(image, 'rb') as file:
            #     binaryData = file.read()
            # image = binaryData
            #image = open(image, 'rb').read()
            #image = base64.b64encode(image)
            # Extracting uploaded data file name
            #photo = secure_filename(image.filename)
            # Upload file to database (defined uploaded folder in static path)
            #image.save(os.path.join(app.config['UPLOAD_FOLDER'], photo))
            # Storing uploaded file path in flask session
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename)))
            #filename = os.path.join(app.config['UPLOAD_FOLDER'], photo)
            photo = image.filename
            #allowed_file(filename)

            #redirect(url_for('static',photo=photo))
            #gal = name + "_profile"
            #img = app.config['UPLOAD_FOLDER'] + gal
            #os.rename(filename,img)

            cur = mysql.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("UPDATE usermast SET image = %s,  job = %s, pointsremember = %s, photo = %s WHERE emailid = %s",
                        (image, job, pointsremember,photo, (session['emailid'],)))
            ms = 'Updated successfully'
            #redirect(url_for('myproj.html', photo=filename))
            mysql.commit()
            cur.close()
            curs = mysql.cursor(MySQLdb.cursors.DictCursor)
            curs.execute('SELECT * FROM usermast WHERE emailid = % s ', (session['emailid'],))
            usermast = curs.fetchone()
            mysql.commit()
    return render_template("profile.html", ms=ms, usermast=usermast)
@app.route("/myproj.html",methods=['POST','GET'])
def myproj():
    if 'loggedin' in session:
        img_file_path = ''
    #     user_image = ''
    #     photo = ''

        if request.method == 'GET':
            cur = mysql.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM usermast WHERE emailid = %s",
                        ((session['emailid'],)))
            usermast = cur.fetchone()
            mysql.commit()

            cur = mysql.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM projmast WHERE emailid = %s",
                        ((session['emailid'],)))
            emailid = cur.fetchall()
            # for projfilepath in emailid:
            #     def write_file(file, projfilepath):
            #         # Convert binary data to proper format and write it on Hard Disk
            #         with open(projfilepath, 'wb') as file:
            #             file.write(projfilepath)

            mysql.commit()
            #img_file_path = session.get('uploaded_img_file_path', None)
        return render_template("myproj.html",usermast=usermast,emailid=emailid)


@app.route("/project.html",methods=['POST','GET'])
def project():
    ms=''
    msg=''
    usermast=''
    filename = ''
    name=''
    user = ''
    if 'loggedin' in session:
        if request.method == 'POST':
            projtitle = request.form['projtitle']
            languages = request.form['languages']
            descriptions = request.form['descriptions']
            projfilepath = request.files['projfilepath']
            #projfilepath.save(secure_filename(projfilepath.filename))
            #projfilepath = projfilepath.filename
            #id = session['id']
            # with open(projfilepath, 'rb') as file:
            #     binaryData = file.read()
            # projfilepath = binaryData

            projfilepath.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(projfilepath.filename) ))
            filename = projfilepath.filename
            #filename = zipfile.ZipFile(projfilepath)
            cur = mysql.cursor(MySQLdb.cursors.DictCursor)

            cur.execute("SELECT name FROM usermast WHERE emailid = %s",
                        ((session['emailid'],)))
            name = cur.fetchone()
            mysql.commit()
            cur = mysql.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('INSERT INTO projmast(projtitle, descriptions, languages, projfilepath, filename, name, emailid) VALUES ( % s, % s, % s, % s, % s, % s, % s)',(projtitle, descriptions, languages, projfilepath, filename, name, session['emailid']))
            mysql.commit()
            ms="Upload Successfully!!!"
    return render_template("project.html",ms=ms)

@app.route("/host")
def host():
        msg=''
        msg = "LOGIN FIRST!!!"
        return  render_template("homepage.html",msg=msg)

@app.route("/liveone")
def live():
    usermast = ''
    if 'loggedin' in session:
        cur = mysql.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM usermast WHERE emailid = %s",((session['emailid'],)))
        usermast = cur.fetchone()
        mysql.commit()
        return  render_template("profile.html",usermast=usermast)

@app.route("/searchform.html", methods=["POST", "GET"])
def searchform():
    return render_template("searchform.html")

@app.route("/ajaxlivesearch", methods=["POST", "GET"])
def ajaxlivesearch():
    projmast = ''
    numrows = ''
    cur = mysql.cursor(MySQLdb.cursors.DictCursor)
    if 'loggedin' in session:
        if request.method == 'POST':
            search_word = request.form['query']
            print(search_word)
            if search_word == '':
                query = "SELECT * from projmast ORDER BY id"
                cur.execute(query)
                projmast = cur.fetchall()
            else:

                query = "SELECT * from projmast WHERE projtitle LIKE '%{}%' OR emailid LIKE '%{}%' OR languages LIKE '%{}%' ORDER BY id DESC LIMIT 20".format(
                    search_word, search_word, search_word)
                cur.execute(query)
                numrows = int(cur.rowcount)
                projmast = cur.fetchall()
                print(numrows)

        return jsonify({'htmlresponse': render_template('response.html', projmast=projmast, numrows=numrows)})

#
# @app.route("/delete")
# def delete():
#     cur = mysql.cursor(MySQLdb.cursors.DictCursor)
#     #     cur.execute('SELECT * FROM usermast WHERE emailid = % s ', (session['emailid'],))
#     #     usermast = cur.fetchone()
#           #sql = "DELETE FROM EMPLOYEE WHERE AGE > '%d'" % (25
#    return  render_template("delete")

@app.route("/contact.html")
def contact():
   return  render_template("contact.html")

@app.route("/about.html")
def about():
   return  render_template("about.html")

@app.route('/logout')
def logout():
	session.pop('emailid', None)
	return redirect('/')

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)