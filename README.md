# Portenta Servo Vision

The Portenta Servo Vision project is a Python Flask web application served from a Raspberry Pi 4 that enables remote control and live video streaming from a Portenta H7 board equipped with a Portenta Vision Shield.

## Directory Structure

Sure, here is a revised version of the README file content:

markdown

# Portenta Servo Vision

The Portenta Servo Vision project is a Python Flask web application served from a Raspberry Pi 4 that enables remote control and live video streaming from a Portenta H7 board equipped with a Portenta Vision Shield.

## Directory Structure
```
portenta-servo-vision/
├── LICENSE
├── README.md
├── app.py
├── firmware
│ └── servo_vision.py
├── requirements.txt
├── static
│ ├── servo.js
│ └── styles.css
└── templates
└── index.html
```

## Hardware Requirements

1. **Raspberry Pi 4:** This is the server host for the Python application. The Raspberry Pi should be connected to a network via Ethernet.

2. **Arduino Portenta H7 and Vision Shield:** This system serves as the client, sending images to the server. The Vision Shield allows for easy image capture, while the Ethernet connection ensures fast and reliable data transmission.

## Setup and Usage

1. **Connection:** Connect the Portenta H7 with Vision Shield and Raspberry Pi 4 to your network via Ethernet.

2. **Server Setup:** On the Raspberry Pi, navigate to the `portenta-servo-vision/` directory and install the necessary Python packages with `pip install -r requirements.txt`. Run the server with `python3 app.py`.

3. **Client Setup:** Upload the `servo_vision.py` script to your Portenta H7 board using the Arduino IDE.

4. **Accessing the Stream:** The live video stream can be accessed by connecting to `http://[raspberry-pi-ip-address]:5000` on a web browser in the same network.

## Contributing

Contributions are welcome! Please read the [contributing guide](CONTRIBUTING.md) for more information.

## License

This project is licensed under the terms of the [MIT license](LICENSE).
