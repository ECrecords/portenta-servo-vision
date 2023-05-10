'''
======================================================================================
File Name: live_stream.py
Author: Elvis Chino-Islas
Date: 10/05/2023
Description: This Python script receives images from a UDP stream and serves them as 
a live video stream over HTTP. The script is designed to be used on a PC.
======================================================================================
'''

import socket
import struct
import io
from flask import Flask, Response, render_template
from PIL import Image

app = Flask(__name__)

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a specific network interface and port number
server_address = ('192.168.0.141', 6060)  # adjust as needed
sock.bind(server_address)

def generate():
    while True:
        # Receive data
        data, address = sock.recvfrom(65507)

        # Use the data as a byte stream for an image
        image_stream = io.BytesIO(data)

        # Open the image with PIL
        image = Image.open(image_stream)

        # Save the image to a byte stream in JPEG format
        byte_stream = io.BytesIO()
        image.save(byte_stream, format='JPEG')
        frame = byte_stream.getvalue()

        # Yield the frame data in the format expected by MJPEG
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='192.168.0.141', port=5000)  # adjust as needed
