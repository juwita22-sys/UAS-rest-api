from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'universitas'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return 'Selamat datang di My Web'

@app.route('/person')
def person():
    return jsonify({'name': 'juwita', 'address': 'Indralaya'})

@app.route('/dosen', methods=['GET', 'POST'])
def dosen():
    cursor = mysql.connection.cursor()
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM DOSEN")
        column_names = [i[0] for i in cursor.description]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        cursor.close()
        return jsonify(data)
    
    elif request.method == 'POST':
        data = request.get_json()
        nama = data.get('nama')
        univ = data.get('univ')
        jurusan = data.get('jurusan')

        sql = "INSERT INTO DOSEN (nama, univ, jurusan) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nama, univ, jurusan))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data berhasil ditambahkan'})

@app.route('/detaildosen')
def detaildosen():
    dosen_id = request.args.get('id')
    if dosen_id:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM DOSEN WHERE dosen_id = %s"
        cursor.execute(sql, (dosen_id,))
        column_names = [i[0] for i in cursor.description]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        cursor.close()
        return jsonify(data)
    else:
        return jsonify({'error': 'Parameter id diperlukan'}), 400

@app.route('/deletedosen', methods=['DELETE'])
def deletedosen():
    dosen_id = request.args.get('id')
    if dosen_id:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM DOSEN WHERE dosen_id = %s"
        cursor.execute(sql, (dosen_id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data berhasil dihapus'})
    else:
        return jsonify({'error': 'Parameter id diperlukan'}), 400

@app.route('/editdosen', methods=['PUT'])
def editdosen():
    dosen_id = request.args.get('id')
    data = request.get_json()

    if dosen_id:
        nama = data.get('nama')
        univ = data.get('univ')
        jurusan = data.get('jurusan')

        cursor = mysql.connection.cursor()
        sql = "UPDATE DOSEN SET nama = %s, univ = %s, jurusan = %s WHERE dosen_id = %s"
        cursor.execute(sql, (nama, univ, jurusan, dosen_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data berhasil diubah'})
    else:
        return jsonify({'error': 'Parameter id diperlukan'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
