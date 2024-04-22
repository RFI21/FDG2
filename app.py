from flask import Flask, render_template, request,redirect,url_for,jsonify
from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime

import os
from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Connect MongoDb
MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app=Flask(__name__)
 
@app.route('/', methods=['GET'])
def home():
    data=list(db.fruit.find({}))
    return render_template('dashboard.html', data=data)

@app.route('/fruit', methods=['GET','POST'])
def fruit():
    fruit=list(db.fruit.find({}))
    return render_template('fruit.html', fruit=fruit)
 
@app.route('/add', methods=['GET','POST'])
def addfruit():
    if request.method == 'POST':
        nama= request.form['nama']
        harga=request.form['harga']
        deskripsi= request.form['deskripsi']
        today = datetime.now()
        mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
        gambar= request.files['gambar']
        

        if gambar:
         
            gambar_asli=gambar.filename
            extensi=gambar_asli.split('.')[-1]
            file_asli=f"img-{mytime}.{extensi}"
            file_path=f'static/assets/ImagePath/img-{mytime}.{extensi}'
            gambar.save(file_path)
        else:
            gambar=None
        
        doc = {
            'nama':nama,
            'harga':harga,
            'gambar':file_asli,
            'deskripsi':deskripsi
        }
        db.fruit.insert_one(doc)
        return redirect(url_for('fruit',message="Data Berhasil Ditambahkan"))
    return render_template('AddFruit.html')

@app.route('/edit/<_id>', methods=['GET','POST'])
def editfruit(_id):
    if request.method == 'POST':
        id = request.form['_id']
        nama = request.form['nama']
        harga = request.form['harga']
        deskripsi = request.form['deskripsi']
        today = datetime.now()
        mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
        gambar = request.files['gambar']

        doc = {
            'nama':nama,
            'harga':harga,
            'deskripsi':deskripsi
        }
        if gambar:

            gambar_asli=gambar.filename
            extensi=gambar_asli.split('.')[-1]
            file_asli=f"img-{mytime}.{extensi}"
            file_path=f"static/assets/ImagePath/img-{mytime}.{extensi}"
            gambar.save(file_path)
            doc['gambar']=file_asli
        db.fruit.update_one({'_id':ObjectId(id)}, {'$set':doc})
        return redirect(url_for('fruit',message="Data Berhasil Diubah"))

    id=ObjectId(_id)
    data=list(db.fruit.find({'_id':id}))
    return render_template('EditFruit.html', data=data[0])
 
@app.route('/delete/<_id>', methods=['GET','POST'])
def deletefruit(_id):
    db.fruit.delete_one({'_id':ObjectId(_id)})
    return redirect(url_for('fruit',message="Data Berhasil Dihapus"))

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug= True)
