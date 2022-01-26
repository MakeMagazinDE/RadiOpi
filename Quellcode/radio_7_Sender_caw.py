#!/usr/bin/python3
# Bibliotheken importieren
import os
import subprocess
import RPi.GPIO as GPIO
import time

# Variante mit zwei Tasten und 7 Sendern (weil 7 LEDs vorhanden waren)
# Carsten Wartmann (caw)



# Nightrider
def kit(count):
   for i in range(count):
	  for s in streams:
		  GPIO.output(s[1], GPIO.HIGH)
		  time.sleep(0.05)
		  GPIO.output(s[1], GPIO.LOW)
	  for s in reversed(streams):
		  GPIO.output(s[1], GPIO.HIGH)
		  time.sleep(0.05)
		  GPIO.output(s[1], GPIO.LOW)


# Stream starten Funktion
def playstream(stream):
	print ("Starte Radio Stream: ",streams[stream][0])
	radio = subprocess.Popen(["mpv", "--cache-secs=2", "--cache-pause=yes", "--cache-pause-wait=2", "--cache-pause-initial=yes",
							  streams[stream][0]],stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	return radio



# Pinbezeichnungen festlegen
GPIO.setmode(GPIO.BCM)

#GPIOS entkoppeln von Streams!

#  Format  "Stream" , LED PIN
streams = [		["https://streams.starfm.de/millennium_rock.mp3",2],
				["https://streamtdy.ir-media-tec.com/live/mp3-128/dmhubweb/play.mp3",3],
				["https://streams.starfm.de/alternative.mp3",4],
				["https://mp3.harmonyfm.de/hrmplus/hq70er.aac",17],
				["https://kinderradio.stream.laut.fm/kinderradio",27],
				["https://streams.starfm.de/classic_rock.mp3",22],
				["https://streams.starfm.de/berlin.mp3",10],
 ]


GPIO.setwarnings(False)
# Pins initialisieren
for s in streams:
	GPIO.setup(s[1], GPIO.OUT, initial=GPIO.LOW) # LED Ausgang

kit(4)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Schalter Zurück Eingang
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Schalter Vor Eingang

# Warten bis System bereit
#time.sleep(10)

streamplay	=  0
oldplay		= -1
start		= 0.0


# Umschreiben mit GPIO.add_event_detect() etc.!
while True:
   if GPIO.input(24) == False or GPIO.input(23) == False:
	  start = time.time()
	  GPIO.output(streams[streamplay][1],GPIO.LOW)
	  if GPIO.input(24) == False:
		 streamplay = (streamplay + 1) % 7
	  if GPIO.input(23) == False:
		 streamplay = (streamplay - 1) % 7
	  print(oldplay,streamplay)
	  GPIO.output(streams[streamplay][1],GPIO.HIGH)
	  time.sleep(0.3)

   if (oldplay!=streamplay and time.time()-start>1.0):
	  if oldplay!=-1:
		 pass
		 radio.kill()
	  print("Play: ",streamplay, time.time()-start)
	  radio=playstream(streamplay)
	  GPIO.output(streams[streamplay][1],GPIO.HIGH)
	  oldplay=streamplay
	  time.sleep(.5)