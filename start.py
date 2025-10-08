import RPi.GPIO as GPIO
import sys
import getopt
import curses
import time
import os
import termios
from multiprocessing import Process, Queue, Lock

import signal

def Exit_gracefully(signal, frame):
    return 0

signal.signal(signal.SIGINT, Exit_gracefully)
signal.signal(signal.SIGTSTP, Exit_gracefully)

globals()['user']=""

def user_input(stdin):
    while 1:
        response = ""
        while (response != "hursley"):
            print("Password:", end='')
            sys.stdout.flush()
            termios.tcflush(stdin, termios.TCIOFLUSH)
            response = stdin.readline()
            response = response.replace("\n","")
            print (response)
            if (response != "hursley"):
                print("Incorrect password, try again......")

        print ("Welcome admin. Your code is 341")

def startp():
    newstdin = os.fdopen(os.dup(sys.stdin.fileno()))    
    q = Queue()
    globals()['user'] = Process(target=user_input, args=(newstdin,))
    globals()['user'].daemon = True
    globals()['user'].start()

def gpio_callback(channel):
    if (GPIO.input(channel) == 1):
        globals()['user'].terminate()
        
        for i in range(0,100):
            print ("")

        for i in range(50,0,-1):
            print ("--------------- ALARM: Terminal approached. Waiting (" + str(i) + ").... -------------")
            time.sleep(1)
        
        startp()

startp()

ch=5
debounce=200

# setup GPIO call back
GPIO.setmode(GPIO.BOARD)
GPIO.setup(ch,GPIO.IN)
GPIO.add_event_detect(ch,GPIO.BOTH,callback=gpio_callback, bouncetime=debounce)
    
while 1:
    x=1
