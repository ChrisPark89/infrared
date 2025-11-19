import time
import signal
import requests
import json
import threading

# Try to import RPi.GPIO; if not available, use a mock version - Test purpose
try:
    import RPi.GPIO as GPIO
    USING_PI = True
    print("Running on Raspberry Pi with real GPIO.")
except ImportError:
    USING_PI = False
    print("Running on non-Pi – using Mock GPIO (no sensor required).")

    class MockGPIO:
        BOARD = "BOARD"
        IN = "IN"
        BOTH = "BOTH"

        def setmode(self, mode): pass
        def setup(self, channel, mode): pass
        def input(self, channel): return 0
        def add_event_detect(self, ch, edge, callback=None, bouncetime=200): pass
        def cleanup(self): pass

    GPIO = MockGPIO()  # Use mock GPIO object


# Exit handler
def Exit_gracefully(signal_num, frame):
    GPIO.cleanup()
    print("Exiting gracefully...")
    exit(0)

signal.signal(signal.SIGINT, Exit_gracefully)
signal.signal(signal.SIGTSTP, Exit_gracefully)

# HTTP Sender
def send_http_request():
    try:
        server_url = 'http://localhost:3000/api/trigger'

        headers = {"Content-Type": "application/json"}
        payload = {"sensor": "test", "status": "triggered"}

        response = requests.post(server_url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            print("HTTP request sent successfully.")
        else:
            print(f"Failed HTTP request. Status: {response.status_code}")
            print("Response:", response.text)

    except Exception as e:
        print(f"Error sending HTTP request: {e}")


# GPIO callback (Pi only)
def gpio_callback(channel):
    if USING_PI and GPIO.input(channel) == 1:
        print("Sensor triggered (real GPIO)! Sending HTTP request...")
        send_http_request()


# Mock trigger for Mac & Pi
def mock_trigger_listener():
    while True:
        input("\nPress ENTER to simulate a sensor trigger...\n")
        print("Mock trigger activated! Sending HTTP request...")
        send_http_request()


# Run mock trigger thread
mock_thread = threading.Thread(target=mock_trigger_listener, daemon=True)
mock_thread.start()

# GPIO Setup (ignored on Mac)
if USING_PI:
    ch = 5
    debounce = 200
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ch, GPIO.IN)
    GPIO.add_event_detect(ch, GPIO.BOTH, callback=gpio_callback, bouncetime=debounce)

# Main loop
while True:
    time.sleep(0.5)
