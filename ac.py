from flask import Flask, render_template, request, send_from_directory
from uuid import uuid4
from os import path
from classifier import *
import sqlite3
import os

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
app.config['APPLICATION_ROOT'] = '/amazonclassifier'
here = os.path.dirname(__file__)


@app.route('/')
def home():
    print("sfasd")
    return send_from_directory('static','upload.html')

@app.route('/uploadReports/', methods=['POST'])
def uploadReports():
    #Setup names
    orderCSVFile=str(uuid4())
    itemsCSVFile=str(uuid4())
    categoriesFile=str(uuid4())
    dbfile=path.join(here,'db',str(uuid4())+".sqlite")
    
    #DB SETUP
    conn = sqlite3.Connection(dbfile)

    #GET FORM
    f = request.files['ordersCSV']
    f.save(path.join(here,'uploads',orderCSVFile))
    f = request.files['itemsCSV']
    f.save(path.join(here,'uploads',itemsCSVFile))
    f = request.files['categories']
    f.save(path.join(here,'uploads',categoriesFile))
    loadreports(conn, path.join(here,'uploads',orderCSVFile),path.join(here,'uploads',itemsCSVFile),path.join(here,'uploads',categoriesFile))
    data=getData(conn)
    categories=getCategories(conn)
    return render_template('dataclassifier.html.jinja',items=data,dbfile=dbfile,categories=categories)

@app.route('/createbankcsv/', methods=["POST"])
def createbankcsv():
    #Get Data
    itemcategory={}
    print(request.form)
    for k in request.form.keys():
        print("asdfasd")
        itemcategory[k]=request.form[k]
    dbfile=request.form['db']
    print(dbfile)
    conn = sqlite3.Connection(dbfile)
    items=getData(conn)
    return(render_template('bankreport.html.jinja',items=items,categories=itemcategory))

@app.route('/instructions')
def instructions():
    return send_from_directory('static','instructions.html')

if __name__ == '__main__':
    app.run(port=5001)
