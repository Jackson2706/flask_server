import requests
from PIL import Image
import io
import datetime
import base64

def upload_data(image, string_data, server_url):
    try:
        # Chuyển đổi ảnh sang chế độ RGB nếu cần
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Chuyển đổi ảnh thành dạng byte
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='JPEG')
        image_bytes = image_bytes.getvalue()

        # Base64 encode dữ liệu ảnh
        encoded_image = base64.b64encode(image_bytes).decode('utf-8')

        # Tạo dictionary chứa dữ liệu
        data = {
            'image': encoded_image,
            'string_data': string_data,
            'timestamp': datetime.datetime.now().isoformat()  # Lấy thời gian hiện tại dưới dạng chuỗi ISO
        }

        # Gửi dữ liệu dưới dạng JSON lên server
        response = requests.post(server_url, json=data)
        if response.status_code == 200:
            print("Data uploaded successfully")
        else:
            print("Failed to upload data. Server response:", response.text)
    except Exception as e:
        print("Error:", e)

# Sử dụng hàm upload_data
image = Image.open("Screenshot from 2024-03-10 16-44-11.png")  # Đọc ảnh từ đường dẫn
string_data = "Jackson"  # Chuỗi dữ liệu
server_url = "http://127.0.0.1:5000/upload"  # Địa chỉ của Flask server
upload_data(image, string_data, server_url)
