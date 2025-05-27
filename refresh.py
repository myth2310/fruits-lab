from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'fruts_classification_app'
mysql = MySQL(app)

with app.app_context():
    cur = mysql.connection.cursor()

    # Nonaktifkan FK check
    cur.execute("SET FOREIGN_KEY_CHECKS = 0")

    # --- USERS ---
    cur.execute("DELETE FROM users")
    cur.execute("ALTER TABLE users DROP id")
    cur.execute("ALTER TABLE users ADD id INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST")

    # --- KANDUNGAN_BUAH ---
    # Cek nama FK
    cur.execute("""
        SELECT CONSTRAINT_NAME 
        FROM information_schema.KEY_COLUMN_USAGE 
        WHERE TABLE_NAME = 'kandungan_buah' 
        AND TABLE_SCHEMA = 'fruts_classification_app' 
        AND REFERENCED_TABLE_NAME IS NOT NULL
    """)
    fk_result = cur.fetchone()

    # Jika ada FK, drop FK
    if fk_result:
        fk_name = fk_result[0]
        print(f"Dropping FK: {fk_name}")
        cur.execute(f"ALTER TABLE kandungan_buah DROP FOREIGN KEY {fk_name}")
    else:
        print("Tidak ada FK yang perlu dihapus di kandungan_buah.")

    # Lanjutkan reset kolom
    cur.execute("DELETE FROM kandungan_buah")
    cur.execute("ALTER TABLE kandungan_buah DROP id")
    cur.execute("ALTER TABLE kandungan_buah ADD id INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST")

    # --- BUAH ---
    cur.execute("DELETE FROM buah")
    cur.execute("ALTER TABLE buah DROP id")
    cur.execute("ALTER TABLE buah ADD id INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST")

    # --- HASIL_QUIS ---
    cur.execute("DELETE FROM hasil_quis")
    cur.execute("ALTER TABLE hasil_quis DROP id")
    cur.execute("ALTER TABLE hasil_quis ADD id INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST")

    # Aktifkan kembali FK
    cur.execute("SET FOREIGN_KEY_CHECKS = 1")

    mysql.connection.commit()
    print("Tabel berhasil di-reset.")
