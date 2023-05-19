'''
======================================================================================
File Name: image_stream.py
Author: Elvis Chino-Islas
Date: 09/05/2023
Description: This Python script captures images from a sensor, compresses them, and
sends them over a network using UDP. The script is designed to be used in an embedded
system context.
======================================================================================
'''

# Importing the necessary libraries
import sensor, image, time
import usocket, network
import gc
from pyb import Servo, Pin, Timer

# Setting the clock
clock = time.clock()

# Setting the IP address and port number
address = ('192.168.0.175', 6060)

# Constants for pan and tilt
PAN_FACTOR = 2
TILT_FACTOR = 2
MAX_PULSEWIDTH = 4200
MIN_PULSEWIDTH = 560
DEFAULT_TILT_PULSEWIDTH = 1000

# Create a Timer object on Timer 3 with a frequency of 50Hz
timer1 = Timer(3, freq=50)

# Create Pin objects for the tilt and pan servo pins
# The tilt servo is on pin "PC6" and the pan servo is on pin "PC7"
# The pins are set to output mode with push-pull type and no pull resistors
tilt_servo_pin = Pin("PC7", Pin.OUT_PP, Pin.PULL_NONE)
pan_servo_pin = Pin("PC6", Pin.OUT_PP, Pin.PULL_NONE)

# Create PWM channels on the Timer for each servo
# The tilt servo is on channel 1 and the pan servo is on channel 2
tilt = timer1.channel(1, Timer.PWM, pin=tilt_servo_pin, pulse_width=DEFAULT_TILT_PULSEWIDTH )
pan = timer1.channel(2, Timer.PWM, pin=pan_servo_pin , pulse_width=MIN_PULSEWIDTH)



def init_sensor():
    '''
    Function to initialize the image sensor.
    '''
    # Resetting the sensor
    sensor.reset()

    # Setting the pixel format to grayscale
    sensor.set_pixformat(sensor.GRAYSCALE)

    # Setting the frame size to QVGA
    sensor.set_framesize(sensor.QVGA)

    # Setting windowing to look at center 240x240 pixels of the VGA resolution
    sensor.set_windowing((240, 240))

    # Skipping frames to allow the camera to adjust to lighting conditions
    sensor.skip_frames(time = 2000)

    # Turning off auto gain to prevent image washout
    sensor.set_auto_gain(False)


def get_closest_face(objects):
    '''
    Function to get the closest face from a list of bounding boxes.
    It assumes the closest face is the one with the largest area.
    '''
    if not objects:
        return None
    else:
        # Sort the list of objects based on the area of the bounding box (width * height)
        objects.sort(key=lambda r: r[2]*r[3], reverse=True)

        # The closest face will be the first object in the sorted list
        return objects[0]


def main():
    '''
    Main function to run the program.
    '''
    # Activating the LAN
    lan = network.LAN()
    lan.active(True)
    lan.ifconfig('dhcp')
    print(lan.ifconfig())

    # Initializing the sensor
    init_sensor()

    # Setting the clock
    clock = time.clock()

    face_cascade = image.HaarCascade("frontalface", stages=25)

    # Infinite loop to continuously capture and send images

    pulse_ms = 1;
    while True:
        clock.tick()

        # Free memory if necessary
        gc.collect()
        free_memory = gc.mem_free()
        print("Free memory: ", free_memory)

        # Check if enough memory is available
        if free_memory < 50000: # adjust this value based on your device's capabilities
            print("Low memory, skipping frame")
            continue

        # Capturing an image
        img = sensor.snapshot()

        objects = img.find_features(face_cascade, threshold=0.75, scale_factor=1.25)

        closest_face = None
        # Find the closest face
        if len(objects) >= 1:
            closest_face = objects[0] #get_closest_face(objects)

        # If a face was found, draw a rectangle around it and center the face
        if closest_face is not None:
            img.draw_rectangle(closest_face)

            # Calculate error between center of image and center of face
            img_width, img_height = img.width(), img.height()  # Assumes you have these methods
            face_x, face_y, face_width, face_height = closest_face
            face_center_x = face_x + face_width // 2
            face_center_y = face_y + face_height // 2

            pan_error = img_width // 2 - face_center_x
            tilt_error = img_height // 2 - face_center_y

            # Adjust servo positions. Clamp values between 1000us and 2000us to avoid damaging the servos.
            pan_pulse_width = min(max(pan.pulse_width() + PAN_FACTOR * pan_error, MIN_PULSEWIDTH), MAX_PULSEWIDTH)
            tilt_pulse_width = min(max(tilt.pulse_width() + TILT_FACTOR * tilt_error, MIN_PULSEWIDTH), MAX_PULSEWIDTH)

            pan.pulse_width(pan_pulse_width)
            tilt.pulse_width(tilt_pulse_width)


        # Compressing the image
        compressed_img = img.compress(50)

         #Creating a socket and sending the image over the network
        sock = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
        sock.sendto(compressed_img, address)
        sock.close()

        del sock
        del img
        del compressed_img

        # Printing the frames per second
        print(clock.fps())

if __name__=='__main__':
    main()
