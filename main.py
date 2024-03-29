# from flask import Flask
from flask import Flask, request, render_template
import os
import sqlite3 as sql
import pandas as pd
import time
import redis
import _pickle as cPickle
import matplotlib
from matplotlib import pyplot as plt
# from matplotlib import *
from sklearn.cluster import KMeans
from scipy.spatial import distance

app = Flask(__name__)

port = int(os.getenv('PORT', 6000))

# @app.route('/')
# def my_form():
#     return render_template('my-form.html')
#
# @app.route('/', methods=['POST'])
# def my_form_post():
#     text = request.form['text']
#     processed_text = text.upper()
#     return processed_text
#
# def hello_world():
#   return 'Hello, World!\n This looks just amazing within 5 minutes'

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/enternew')
def upload_csv():
    return render_template('upload.html')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':

        con = sql.connect("database.db")
        csv = request.files['myfile']
        file = pd.read_csv(csv)
        file.to_sql('Earthquake', con, schema=None, if_exists='replace', index=True, index_label=None, chunksize=None,
                    dtype=None)
        con.close()
        return render_template("result.html", msg="Record inserted successfully")

@app.route('/clustering')
def clustering():
    query = "SELECT latitude,longitude FROM Earthquake "
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    y = pd.DataFrame(rows)
    k = KMeans(n_clusters=5, random_state=0).fit(y)
    centroids = k.cluster_centers_
    X = y.dropna()
    print(X[0])
    fig = plt.figure()
    plt.scatter(X[0], X[1])
    plt.scatter(centroids[:,0],centroids[:,1],color='black')
    # print(X[:,0])
    #display popup
    plt.show()
    fig.savefig('static/img.png')
    # print(k.cluster_centers_)
    return render_template("clus.html", data=rows, kmeansCentroid = centroids)


@app.route('/list')
def list():
    start_time = time.time()
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("select * from Earthquake")
    rows = cur.fetchall();
    end_time=time.time()-start_time
    con.close()
    return render_template("list.html", rows=rows, time=end_time)

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=port,debug=True)
