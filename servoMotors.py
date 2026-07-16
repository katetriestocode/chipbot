import random
import threading
import time

from gpiozero import Device, AngularServo
from gpiozero.pins.lgpio import LGPIOFactory

Device.pin_factory = LGPIOFactory()

LEFT_SERVO = 12
RIGHT_SERVO = 13

EMOTIONS = {
    "HAPPY":    (40, 75, 0.08, 0.18),
    "EXCITED":  (65, 90, 0.04, 0.10),
    "CURIOUS":  (20, 55, 0.18, 0.40),
    "THINKING": (8, 25, 0.40, 0.80),
    "CONFUSED": (35, 70, 0.12, 0.25),
    "SLEEPY":   (5, 15, 0.60, 1.00),
    "THANKFUL": (25, 55, 0.12, 0.25),
    "NEUTRAL":  (10, 35, 0.20, 0.50),
}

class ServoMotors:

    def __init__(self):

        self.left = AngularServo(
            LEFT_SERVO,
            min_angle=-90,
            max_angle=90,
            min_pulse_width=0.0005,
            max_pulse_width=0.0025
        )

        self.right = AngularServo(
            RIGHT_SERVO,
            min_angle=-90,
            max_angle=90,
            min_pulse_width=0.0005,
            max_pulse_width=0.0025
        )

        self.lock = threading.Lock()

        self.running = True
        self.emotion = "NEUTRAL"

        self.left.angle = 0
        self.right.angle = 0

        self.thread = threading.Thread(
            target=self._loop,
            daemon=True
        )
        self.thread.start()

    def react(self):
        with self.lock:

            self.left.angle = 35
            self.right.angle = -35

            time.sleep(0.10)

            self.left.angle = 0
            self.right.angle = 0

    def set_emotion(self, emotion):

        emotion = emotion.upper()

        if emotion not in EMOTIONS:
            emotion = "NEUTRAL"

        self.emotion = emotion

    def _loop(self):

        while self.running:

            min_amp, max_amp, min_speed, max_speed = EMOTIONS[self.emotion]

            amp = random.randint(min_amp, max_amp)

            if random.random() < 0.5:
                amp = -amp

            if random.random() < 0.12:
                amp = random.choice([-1, 1]) * random.randint(75, 90)

            speed = random.uniform(min_speed, max_speed)

            with self.lock:

                self.left.angle = amp
                self.right.angle = -amp

            time.sleep(speed)

            if random.random() < 0.20:
                time.sleep(random.uniform(0.5, 1.0))
            else:
                time.sleep(random.uniform(0.03, 0.15))

    def stop(self):

        self.running = False

        self.thread.join()

        self.left.angle = 0
        self.right.angle = 0

        time.sleep(0.2)

        self.left.detach()
        self.right.detach()
