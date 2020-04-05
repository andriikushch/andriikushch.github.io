import RPi.GPIO as GPIO
import getch
import sys

print("start")

# Change the mode to the BCM, to use known GPIO's mapping
GPIO.setmode(GPIO.BCM)

# Define a constants to have a reasonable names for the GPIOs
ENA = 13
ENB = 20
IN1 = 19
IN2 = 16
IN3 = 21
IN4 = 26

# Set the initial state for the GPIOs: mode OUT, value LOW
GPIO.setup(ENA, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ENB, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)

# Turn on the motors, by setting signal to HIGH
GPIO.output(ENA, True)
GPIO.output(ENB, True)

# Create a PWM instance, with initial frequency
p1 = GPIO.PWM(ENA, 60)
p2 = GPIO.PWM(ENB, 60)

# Start PWM
p1.start(0)
p2.start(0)

# Set initial speed
speed = 0


# Rotate motors forward
def forward():
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)


# Rotate motors backward
def backward():
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)


# Right motor forward, left backward
def left():
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)


# Left motor forward, right backward
def right():
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)


# Set all GPIOs to low, to stop the vehicle
def stop():
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, False)


# Increase speed by 10%
def increase_speed():
    global p1, p2, speed
    if speed < 100:
        speed += 10
        p1.ChangeDutyCycle(speed)
        p2.ChangeDutyCycle(speed)


# Decrease speed by 10%
def decrease_speed():
    global p1, p2, speed
    if speed > 0:
        speed -= 10
        p1.ChangeDutyCycle(speed)
        p2.ChangeDutyCycle(speed)


# Implement vehicle control
def switch(x):
    return {
        'w': lambda: forward(),
        's': lambda: backward(),
        'a': lambda: left(),
        'd': lambda: right(),
        'h': lambda: stop(),
        ']': lambda: increase_speed(),
        '[': lambda: decrease_speed(),
    }[x]


# Main loop
while True:
    # Read char from input
    char = getch.getch()
    try:
        # Try to find and run proper control
        switch(char)()
    except KeyError:
        # If unknown control was requested, stop the loop
        break
    print(f"\rspeed {speed}%", end="")
    sys.stdout.flush()

# Reset all GPIOs configured by this command
GPIO.cleanup()

print("end")
