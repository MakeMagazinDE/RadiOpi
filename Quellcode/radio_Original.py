#!/usr/bin/python3
# Bibliotheken importieren
import os
import subprocess
import RPi.GPIO as GPIO
import time

# Pinbezeichnungen festlegen
GPIO.setmode(GPIO.BCM)

# Pins initialisieren
GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW) # LED Sender 1
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Schalter Sender 1
GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW) # LED Sender 2
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Schalter Sender 2

# Warten bis System bereit
time.sleep(10)

# Sender 1 starten
radio = subprocess.Popen(["mpv", "http://stream.bayerwaldradio.com/bayerwaldradio-aac"],stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
print ("Radio Blasmusik gestartet")
# LED 1 anschalten
GPIO.output(23, GPIO.LOW)
GPIO.output(17, GPIO.HIGH)
time.sleep(.1)

# Endlosschleife - auf Knopfdruck warten und Sender starten
while True:
        if GPIO.input(27) == False:
                # Sender 1 starten
                radio.kill()
                time.sleep(.1)
                radio = subprocess.Popen(["mpv", "https://bayerwald.ip-streaming.net/allesblasmusik-aac"],stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                print ("Radio Blasmusik gestartet")
                # LED anschalten
                GPIO.output(23, GPIO.LOW)
                GPIO.output(17, GPIO.HIGH)
                # warten
                time.sleep(1)
        if GPIO.input(24) == False:
                # Sender 2 starten
                radio.kill()
                time.sleep(.1)
                radio = subprocess.Popen(["mpv", "https://schwany.streampanel.cloud/10-blaess"],stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                print ("Radio Blaess gestartet")
                # LED anschalten
                GPIO.output(17, GPIO.LOW)
                GPIO.output(23, GPIO.HIGH)
                # warten
                time.sleep(1)
        time.sleep(.1)