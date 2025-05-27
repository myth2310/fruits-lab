from flask import Flask, render_template, request, redirect, url_for, flash,jsonify, session
from flask_mysqldb import MySQL
import os
from werkzeug.utils import secure_filename
import base64
import io
from PIL import Image
import random
from gtts import gTTS
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import uuid
import random
from datetime import datetime
from werkzeug.security import check_password_hash

app = Flask(__name__)
mysql = MySQL(app)
app.secret_key = 'rahasia'

model = load_model('model_klasifikasi_buah.h5')

class_indices = {'apel hijau': 0, 'apel merah': 1, 'unknown': 2}
index_to_class = {v: k for k, v in class_indices.items()}

img_height, img_width = 100, 100

# Konfigurasi MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'fruts_classification_app'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

app.config['UPLOAD_FOLDER'] = 'static/uploads/buah'
app.config['SOUND_FOLDER'] = 'static/uploads/sounds'
app.config['UPLOAD_KLASIFIKASI'] = 'static/uploads/klasifikasi'

# Dashborad Page
@app.route('/admin/dashboard')
def dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('adminLogin'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) AS total_buah FROM buah")
    jumlah_buah = cur.fetchone()['total_buah']

    cur.execute("SELECT COUNT(*) AS total_kandungan FROM kandungan_buah")
    jumlah_kandungan = cur.fetchone()['total_kandungan']
    return render_template('admin/dashboard-page.html',
                           jumlah_buah=jumlah_buah,
                           jumlah_kandungan=jumlah_kandungan)


@app.route('/admin/buah')
def buah():
    if 'admin_id' not in session:
        return redirect(url_for('adminLogin'))
    
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM buah")
    hasil = cursor.fetchall()
    cursor.close()
    data = []
    for row in hasil:
        data.append({
            'nama_buah': row['nama_buah'],
            'gambar_buah': row['gambar_buah']
        })


    return render_template('admin/buah/index.html', data=data)

@app.route('/admin/buah/create')
def buahCreate():
    if 'admin_id' not in session:
        return redirect(url_for('adminLogin'))
    return render_template('admin/buah/create.html')

@app.route('/admin/buah/store', methods=['GET', 'POST'])
def tambah_buah():
    if 'admin_id' not in session:
        return redirect(url_for('adminLogin'))
    
    if request.method == 'POST':
        nama_buah = request.form['nama_buah']
        file = request.files['gambar_buah']

        if file and nama_buah:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO buah (nama_buah, gambar_buah) VALUES (%s, %s)", (nama_buah, filename))
            mysql.connection.commit()
            cursor.close()
            try:
                tts = gTTS(text=nama_buah, lang='id')
                suara_path = os.path.join(app.config['SOUND_FOLDER'], f"{nama_buah.lower()}.mp3")
                tts.save(suara_path)
                print(f"Suara disimpan: {suara_path}")
            except Exception as e:
                print("Gagal membuat suara:", e)

            flash('Data buah berhasil disimpan dan suara berhasil dibuat!', 'success')
            return redirect(url_for('buah'))

    return redirect('/admin/buah')


@app.route('/admin/kandungan')
def kandungan_buah():
    if 'admin_id' not in session:
        return redirect(url_for('adminLogin'))
    
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT 
            buah.nama_buah,
            buah.gambar_buah,
            kandungan_buah.kandungan
        FROM buah
        INNER JOIN kandungan_buah ON buah.id = kandungan_buah.id_buah
    """)
    hasil = cursor.fetchall()
    cursor.close()

    data = []
    for row in hasil:
        data.append({
            'nama_buah': row['nama_buah'],
            'gambar_buah': row['gambar_buah'],
            'kandungan': row['kandungan']
        })

    return render_template('admin/manfaat/index.html', data=data)

@app.route('/admin/kandungan/create')
def kandunganCreate():
    if 'admin_id' not in session:
        return redirect(url_for('adminLogin'))
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nama_buah FROM buah")
    buah_list = cursor.fetchall()  
    cursor.close()
    return render_template('admin/manfaat/create.html', buah_list=buah_list)

@app.route('/admin/kandungan/store', methods=['POST'])
def kandungan_store():
    if 'admin_id' not in session:
        return redirect(url_for('adminLogin'))
    id_buah = request.form['id_buah']
    kandungan = request.form['kandungan']

    cursor = mysql.connection.cursor()
    cursor.execute("""
            INSERT INTO kandungan_buah (id_buah, kandungan) 
            VALUES (%s, %s)
        """, (id_buah, kandungan))
    mysql.connection.commit()
    return redirect('/admin/kandungan')


#Auth
@app.route('/admin/login', methods=['GET', 'POST'])
def adminLogin():
    if 'admin_id' in session:
        return redirect(url_for('adminDashboard'))  

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND role = 'admin'", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            session['admin_id'] = user['id']
            session['admin_username'] = user['username']
            flash('Login berhasil', 'success')
            return redirect('/admin/dashboard') 
        else:
            flash('Username atau password salah', 'danger')

    return render_template('auth/login.html')

@app.route('/admin/logout')
def adminLogout():
    session.clear()
    return redirect(url_for('adminLogin'))

# Landing Page
@app.route('/')
def index():
    background = url_for('static', filename='bg.jpg')
    return render_template('landing/home-page.html', background=background)


@app.route('/menu')
def menu():
    background = url_for('static', filename='bg-menu.jpg')
    return render_template('landing/menu-page.html',background=background)

@app.route('/kenali-buah')
def kenali_buah():
    cur = mysql.connection.cursor()
    cur.execute("SELECT nama_buah, gambar_buah FROM buah") 
    rows = cur.fetchall()
    buah_list = []
    for row in rows:
        nama = row['nama_buah']
        gambar = url_for('static', filename=f'uploads/buah/{row["gambar_buah"]}')

        suara = url_for('static', filename=f'uploads/sounds/{nama.lower()}.mp3')
        buah_list.append({"nama": nama, "gambar": gambar, "suara": suara})
    return render_template('landing/kenali_buah.html', buah_list=buah_list, )

data_buah_global = []

def ambil_soal():
    cur = mysql.connection.cursor()
    cur.execute("SELECT nama_buah, gambar_buah FROM buah")
    rows = cur.fetchall()

    data_buah = []
    for row in rows:
        # row = (nama_buah, gambar_buah)
        gambar_path = f'static/uploads/buah/{row["gambar_buah"]}'
        data_buah.append({
            "jawaban": row["nama_buah"],
            "gambar": gambar_path
        })
    
    print(data_buah)



    random.shuffle(data_buah)
    # batasi 10 soal saja
    return data_buah[:10]

@app.route('/kuis-buah')
def kuisBuah():
    # Ambil soal 10 buah, simpan di session atau global (lebih baik session untuk multi user)
    soal = ambil_soal()
    session['data_buah'] = soal
    session['hasil_jawaban'] = [None] * len(soal)  # untuk menyimpan jawaban benar/salah tiap soal

    # buat opsi list gabungan dari semua nama buah, random 3 pilihan + jawaban yang benar
    semua_nama = [s['jawaban'] for s in soal]
    opsi_list_all = list(set(semua_nama))
    
    # Untuk tiap soal, buat opsi dengan jawaban benar + 2 opsi random lain (total 3 opsi)
    opsi_list_per_soal = []
    for s in soal:
        opsi = set()
        opsi.add(s['jawaban'])
        while len(opsi) < 3 and len(opsi) < len(opsi_list_all):
            opsi.add(random.choice(opsi_list_all))
        opsi_list_per_soal.append(random.sample(list(opsi), len(opsi)))

    return render_template(
    'landing/kuis-page.html',
    data_buah=soal,
    opsi_list_per_soal=opsi_list_per_soal,
    zip=zip  # <--- tambahkan ini
)

@app.route('/cek-jawaban', methods=['POST'])
def cek_jawaban():
    user_jawaban = request.json.get('jawaban')
    nama_user = request.json.get('nama_user')
    index = int(request.json.get('index'))

    data_buah = session.get('data_buah', [])
    hasil_jawaban = session.get('hasil_jawaban', [])

    if not data_buah or index >= len(data_buah):
        return jsonify({"benar": False, "jawaban": "Tidak diketahui", "selesai": False})

    jawaban_benar = data_buah[index]['jawaban']
    benar = user_jawaban.lower() == jawaban_benar.lower()

    # Simpan hasil jawaban benar/salah ke session
    hasil_jawaban[index] = benar
    session['hasil_jawaban'] = hasil_jawaban

    selesai = all(ans is not None for ans in hasil_jawaban)

    # Jika sudah selesai, simpan nilai ke DB
    if selesai:
      
        nilai = sum(1 for ans in hasil_jawaban if ans)
        nilai_skala = nilai * 10
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO hasil_quis (nama_user, skor) VALUES (%s, %s)",
            (nama_user, nilai_skala)
        )
        mysql.connection.commit()
                                                                                                                                                                                                                                                                                        
    return jsonify({
        "benar": benar,
        "jawaban": jawaban_benar,
        "selesai": selesai,
        "nilai": sum(1 for ans in hasil_jawaban if ans) if selesai else None
    })


@app.route('/skor')
def skor():
    background = url_for('static', filename='bg-menu.jpg')
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT nama_user, skor, tanggal 
        FROM hasil_quis 
        ORDER BY skor DESC, tanggal ASC 
        LIMIT 10
    """)
    skor_teratas = cur.fetchall()
    return render_template('landing/skor-page.html', skor_teratas=skor_teratas,background=background)


@app.route('/klasifikasi-buah', methods=['GET', 'POST'])
def klasifikasiBuah():
    predicted_class = None
    confidence = None
    manfaat = None
    filename = None

    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file:
            # Simpan file
            filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
            filepath = os.path.join(app.config['UPLOAD_KLASIFIKASI'], filename)
            file.save(filepath)

            # Preprocessing gambar
            img = image.load_img(filepath, target_size=(img_height, img_width))
            img_array = image.img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            # Prediksi
            predictions = model.predict(img_array)
            predicted_index = np.argmax(predictions[0])
            predicted_class = index_to_class[predicted_index]
            confidence = float(predictions[0][predicted_index])  # convert to float for safety

            # Ambil manfaat dari DB jika bukan "unknown"
            if predicted_class.lower() != "unknown":
                cursor = mysql.connection.cursor()
                query = """
                    SELECT kandungan FROM kandungan_buah kb
                    JOIN buah b ON kb.id_buah = b.id
                    WHERE b.nama_buah = %s
                    LIMIT 1
                """
                cursor.execute(query, (predicted_class,))
                hasil = cursor.fetchone()
                cursor.close()

                manfaat = hasil['kandungan'] if hasil else "Manfaat belum tersedia untuk buah ini."
            else:
                manfaat = "Gambar belum dikenali dalam sistem ini"

    return render_template('landing/klasifikasi-buah-page.html',
                           filename=filename,
                           predicted_class=predicted_class,
                           confidence=confidence,
                           manfaat=manfaat)



