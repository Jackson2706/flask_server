import requests                 # Import the requests library for making HTTP requests
from PIL import Image           # Import the Image module from the Pillow library for image processing
import io                       # Import the io module for working with bytes data
import datetime                 # Import the datetime module for working with time
import base64                   # Import the base64 module for encoding and decoding base64 data

def upload_data(image, string_data, server_url):
    """
    The upload_data function is used to send image and string data to the server.
    
    Inputs:
    - image: Image object (already opened) to be sent to the server.
    - string_data: String data to be sent to the server.
    - server_url: URL address of the Flask server to send the request.

    Outputs:
    No return value. The result of the data upload process will be printed to the screen.
    """
    try:
        # Convert the image to RGB mode if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Convert the image to bytes
        image_bytes = io.BytesIO()                 # Create a BytesIO object to store the image data as bytes
        image.save(image_bytes, format='JPEG')     # Save the image to the BytesIO object in JPEG format
        image_bytes = image_bytes.getvalue()       # Get the bytes value from the BytesIO object

        # Base64 encode the image data
        encoded_image = base64.b64encode(image_bytes).decode('utf-8')  # Encode the image data to base64 and decode to string

        # Create a dictionary to store the data
        data = {
            'image': encoded_image,                                      # Encoded base64 image data
            'name': string_data,                                   # String data
            'timestamp': datetime.datetime.now().isoformat()             # Current time in ISO format
        }

        # Send the data as JSON to the server
        response = requests.post(server_url, json=data)                   # Send a POST request with JSON data to the server
        if response.status_code == 200:                                   # If the request is successful
            print("Data uploaded successfully")                           # Print success message
        else:
            print("Failed to upload data. Server response:", response.text)  # Print error message if unsuccessful
    except Exception as e:
        print("Error:", e)                                               # Print error if any occurs

def get_data(server_url):
    """
    The get_data function is used to retrieve data from the server.

    Inputs:
    - server_url: URL address of the Flask server to send the data retrieval request.

    Outputs:
    No return value. Information about the data received from the server will be printed to the screen.
    """
    try:
        response = requests.get(server_url)                               # Send a GET request to the server
        if response.status_code == 200:                                   # If the request is successful
            data = response.json()                                        # Convert the received data to a JSON object
            print("Data retrieved successfully:")                         # Print success message
            for item in data['data']:                                     # Iterate through each record in the received data
                # Convert image data from base64 back to bytes
                image_bytes = base64.b64decode(item[0])                    # Decode the base64 image data to bytes
                
                # Open image from bytes
                image = Image.open(io.BytesIO(image_bytes))                # Create an image object from the bytes data
                
                # Save image to file
                image.save(f"image {item[2]}.png")                        # Save the image to a PNG file
                
                # Print image details
                print("Name:", item[1])                                   # Print the name
                print("Timestamp:", item[2])                              # Print the timestamp
                print()                                                    # Print a blank line between each record
        else:
            print("Failed to retrieve data. Server response:", response.text)  # Print error message if unsuccessful
    except Exception as e:
        print("Error:", e)                                                 # Print error if any occurs

# Use the upload_data function
image = Image.open("Screenshot from 2024-03-10 16-44-11.png")             # Read the image from the path
string_data = "Jackson"                                                   # String data
server_url = "http://127.0.0.1:5000/get_data"                             # URL of the Flask server
# upload_data(image, string_data, server_url)                              # Send data to the server
get_data(server_url=server_url)                                           # Retrieve data from the server
