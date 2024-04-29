from flask import Flask, request, jsonify
import os
import sqlite3
import base64

app = Flask(__name__)
DATABASE_PATH = "database.sqlite3"
DATABASE_NAME = "face_data"

@app.before_request
def init_db():
    """
    Initialize the SQLite database.
    Create the 'face_data' table if it doesn't exist.
    """
    if not os.path.exists(DATABASE_PATH):
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {DATABASE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image BLOB,
                name TEXT,
                timestamp TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

def save_data_to_db(image_bytes, name_data, timestamp):
    """
    Save data to the 'face_data' table in the SQLite database.

    Parameters:
    - image_bytes: Bytes data of the image.
    - name_data: Name associated with the image.
    - timestamp: Timestamp when the data is saved.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(f'''
        INSERT INTO {DATABASE_NAME} (image, name, timestamp)
        VALUES (?, ?, ?)
    ''', (sqlite3.Binary(image_bytes), name_data, timestamp))
    conn.commit()
    conn.close()

def get_data_from_db():
    """
    Retrieve all data from the 'face_data' table in the SQLite database.

    Returns:
    - data: Fetched data from the database.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT image, name, timestamp FROM {DATABASE_NAME}")
    data = cursor.fetchall()
    conn.close()
    return data

@app.route('/upload', methods=['POST'])
def upload_data():
    """
    Handle data upload requests.

    Returns:
    - Response JSON indicating success or failure.
    """
    try:
        data = request.json
        image_bytes = base64.b64decode(data['image'])
        string_data = data['name']
        timestamp = data['timestamp']
        save_data_to_db(image_bytes, string_data, timestamp)
        return jsonify({'message': 'Data uploaded successfully'}), 200
    except Exception as e:
        return jsonify({'message': 'Error uploading data', 'error': str(e)}), 500

@app.route('/get_data', methods=['GET'])
def get_data():
    """
    Retrieve data from the 'face_data' table in the SQLite database.

    Returns:
    - Response JSON containing the retrieved data.
    """
    try:
        data = get_data_from_db()
        processed_data = []
        for item in data:
            image_bytes = base64.b64encode(item[0]).decode('utf-8')
            processed_data.append((image_bytes, item[1], item[2]))
        return jsonify({'data': processed_data}), 200
    except Exception as e:
        return jsonify({'message': 'Error getting data', 'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
