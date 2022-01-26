#!/usr/bin/python3
# Bibliotheken importieren
import os
import subprocess
import RPi.GPIO as GPIO
import time

# Pinbezeichnungen festlegen
GPIO.setmode(GPIO.BCM)

# Hier können weitere Zeilen pro Taster eingefügt werden, siehe 3. Zeile
# Format          "Stream" ,             LED-PIN, Taster-PIN
streams = [     ["https://streams.starfm.de/millennium_rock.mp3",17,27],
				["https://streamtdy.ir-media-tec.com/live/mp3-128/dmhubweb/play.mp3",23,24],
#                ["https://streams.starfm.de/alternative.mp3",7,8],
]
streamplay	= 0

# Pins initialisieren
for s in streams:
	GPIO.setup(s[1], GPIO.OUT, initial=GPIO.LOW) # LED Ausgang
	GPIO.setup(s[2], GPIO.IN, pull_up_down=GPIO.PUD_UP) # Schalter Eingang

# Warten bis System bereit
time.sleep(10)

# Stream starten Funktion
def playstream(stream):
	print ("Starte Radio Stream: ",streams[stream][0])
	radio = subprocess.Popen(   ["mpv", "--cache-secs=2", "--cache-pause=yes",
                                "--cache-pause-wait=2", "--cache-pause-initial=yes",
                                streams[stream][0]],stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	for s in streams:
		GPIO.output(s[1],GPIO.LOW)
	GPIO.output(streams[stream][1], GPIO.HIGH)
	return radio


# Default Stream
radio=playstream(streamplay)

# Endlosschleife - auf Knopfdruck checken und Sender starten
while True:
	for index,s in enumerate(streams):
		time.sleep(0.05)
		if GPIO.input(s[2]) == False and streamplay!=index:
				# Sender starten
				radio.kill()
				time.sleep(.2)
				radio=playstream(index)
				streamplay=index