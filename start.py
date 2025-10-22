import RPi.GPIO as GPIO
import time
import signal
import requests
import keyboard  # Import keyboard module to capture key presses

def Exit_gracefully(signal, frame):
    GPIO.cleanup()
    print("Exiting gracefully...")
    exit(0)

signal.signal(signal.SIGINT, Exit_gracefully)
signal.signal(signal.SIGTSTP, Exit_gracefully)

def send_http_request():
    try:
        server_url = '127.0.0.1' # Change this address to the scoreboard server address
        response = requests.post(server_url, json={"sensor_triggered": True}) # Change the json format to the server's spec
        
        if response.status_code == 200:
            print("HTTP request sent successfully.")
        else:
            print(f"Failed to send HTTP request. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error occurred while sending HTTP request: {e}")

def gpio_callback(channel):
    if (GPIO.input(channel) == 1): # sensor gets triggered
        print("Sensor triggered! Sending HTTP request...")
        send_http_request()

ch = 5
debounce = 200

# setup GPIO call back for sensor
GPIO.setmode(GPIO.BOARD)
GPIO.setup(ch,GPIO.IN)
GPIO.add_event_detect(ch, GPIO.BOTH, callback=gpio_callback, bouncetime=debounce)
    
while 1:
    time.sleep(0.5)
