from flask import Flask
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'fruts_classification_app'
mysql = MySQL(app)

with app.app_context():
    cur = mysql.connection.cursor()

    # Nonaktifkan sementara pemeriksaan foreign key
    cur.execute("SET FOREIGN_KEY_CHECKS = 0")

    # Users
    cur.execute("DELETE FROM users")
    cur.execute("ALTER TABLE users DROP id")
    cur.execute("ALTER TABLE users ADD id INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST")

    # Kandungan Buah
    cur.execute("DELETE FROM kandungan_buah")

    # Hapus constraint foreign key terlebih dahulu
    cur.execute("ALTER TABLE kandungan_buah DROP FOREIGN KEY kandungan_buah_ibfk_1")

    # Baru drop kolom id
    cur.execute("ALTER TABLE kandungan_buah DROP id")
    cur.execute("ALTER TABLE kandungan_buah ADD id INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST")

    # Buah
    cur.execute("DELETE FROM buah")
    cur.execute("ALTER TABLE buah DROP id")
    cur.execute("ALTER TABLE buah ADD id INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST")

    # Skor
    cur.execute("DELETE FROM hasil_quis")
    cur.execute("ALTER TABLE hasil_quis DROP id")
    cur.execute("ALTER TABLE hasil_quis ADD id INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST")

    # Aktifkan kembali pemeriksaan foreign key
    cur.execute("SET FOREIGN_KEY_CHECKS = 1")

    mysql.connection.commit()
