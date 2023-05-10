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

# Setting the clock
clock = time.clock()

# Setting the IP address and port number
address = ('192.168.0.141', 6060)

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

        for r in objects:
            img.draw_rectangle(r)


        # Compressing the image
        compressed_img = img.compress(50)

        # Creating a socket and sending the image over the network
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
