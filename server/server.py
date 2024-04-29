from flask import Flask, request, jsonify
import os
import sqlite3
import base64


app = Flask(__name__)
DATABASE_PATH = "database.sqlite3"
DATABASE_NAME = "face_data"

@app.before_request
def init_db():
    if not os.path.exists(DATABASE_PATH):
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(f'''
                CREATE TABLE {DATABASE_NAME}
                       (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       image BLOB,
                       name TEXT,
                       timestamp TIMESTAMP)
            ''')
        conn.commit()
        conn.close()


def save_data_to_db(image_bytes, name_data, timestamp):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {DATABASE_NAME} (image, name, timestamp) VALUES (?, ?, ?)", (sqlite3.Binary(image_bytes), name_data, timestamp))
    conn.commit()
    conn.close()


@app.route('/upload', methods=['POST'])
def upload_data():
    try:
        data = request.json
        image_bytes = base64.b64decode(data['image'])  # Giải mã dữ liệu ảnh từ base64
        string_data = data['string_data']
        timestamp = data['timestamp']

        save_data_to_db(image_bytes, string_data, timestamp)
        return jsonify({'message': 'Data uploaded successfully'}), 200
    except Exception as e:
        return jsonify({'message': 'Error uploading data', 'error': str(e)}), 500
    

if __name__ == "__main__":
    app.run(debug=True)