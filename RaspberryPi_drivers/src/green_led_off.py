import RPi.GPIO as gp

gp.setmode(gp.BCM)
gp.setup(35, gp.OUT)
gp.setup(35, gp.LOW)