from flask import Flask, Response, render_template, jsonify, request
import cv2
import serial
import random
import time

app = Flask(__name__)
arduino_port = '/dev/ttyUSB0'  # Replace with your Arduino's port
baud_rate = 9600

# Initialize serial communication
try:
    arduino = serial.Serial(arduino_port, baud_rate)
    time.sleep(2)  # Wait for the connection to establish
    print("Connected to Arduino")
except serial.SerialException:
    print(f"Error: Could not open serial port {arduino_port}")
    exit()

# Function to send message to Arduino
def send_message(message):
    arduino.write(message.encode())  # Send message as bytes
    print(f"Sent: {message}")

# Initialize the camera capture (0 is the default webcam)
camera = cv2.VideoCapture(0)

# Function to generate video frames
def generate_frames():
    while True:
        success, frame = camera.read()  # Capture frame-by-frame
        if not success:
            break
        else:
            # Encode the frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame in byte format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route to serve the webcam feed
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Route to serve the webpage
@app.route('/')
def index():
    return render_template('index.html')

# Route to get sensor data
@app.route('/sensor_data')
def sensor_data():
    # Simulating two sensor readings
    sensor1_value = random.uniform(7.25, 7.8)  # Example: temperature sensor
    sensor2_value = random.uniform(250, 280)  # Example: humidity sensor
    return jsonify(sensor1=sensor1_value, sensor2=sensor2_value)

# Route to handle button press
@app.route('/button_press', methods=['POST'])
def button_press():
    print("button click")  # Print when button is clicked
    send_message("1")
    return jsonify(status="Button pressed!")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
