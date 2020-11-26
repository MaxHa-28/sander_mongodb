import pymongo
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
client = pymongo.MongoClient('localhost', username='root', password='example', port=27017)

@app.route('/')
def index():
    dbs = client.list_database_names()
    return render_template('index.html', dbs=dbs)

@app.route('/database/<db>')
def database(db):
    collections = client[db].list_collection_names()
    return render_template('db_view.html', db=db, collections=collections)

@app.route('/collection/<db>/<collection>')
def collection(db, collection):
    documents = client[db][collection].find()
    return render_template('collection_view.html', db=db, collection=collection, documents=documents)


@app.route('/create_doc', methods=['POST'])
def create_doc():
    db_name = request.form.get('db_name')
    col_name = request.form.get('col_name')
    key = request.form.get('key')
    value = request.form.get('value')
    client[db_name][col_name].insert_one({key: value})
    return redirect(url_for('index'))
