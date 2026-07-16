import random
import threading
import time

from gpiozero import AngularServo

LEFT_SERVO = 12
RIGHT_SERVO = 13

EMOTIONS = {
    "HAPPY":     (35, 55, 0.16, 0.22),
    "EXCITED":   (60, 85, 0.08, 0.12),
    "CURIOUS":   (25, 40, 0.30, 0.40),
    "THINKING":  (15, 30, 0.50, 0.70),
    "CONFUSED":  (45, 65, 0.20, 0.30),
    "SLEEPY":    (8, 18, 0.70, 0.90),
    "THANKFUL":  (30, 45, 0.22, 0.30),
    "NEUTRAL":   (18, 30, 0.40, 0.55),
}

class ServoMotors:

    def __init__(self):

        self.left = AngularServo(
            LEFT_SERVO,
            min_angle=-90,
            max_angle=90
        )

        self.right = AngularServo(
            RIGHT_SERVO,
            min_angle=-90,
            max_angle=90
        )

        self.lock = threading.Lock()

        self.emotion = "NEUTRAL"
        self.running = True

        self.left.angle = 0
        self.right.angle = 0

        self.thread = threading.Thread(
            target=self._loop,
            daemon=True
        )

        self.thread.start()

    def react(self):
        with self.lock:
            self.left.angle = 15
            self.right.angle = -15

            time.sleep(0.08)

            self.left.angle = 0
            self.right.angle = 0

    def set_emotion(self, emotion):
        emotion = emotion.upper()

        if emotion not in EMOTIONS:
            emotion = "NEUTRAL"

        self.emotion = emotion

    def _move(self, amp, speed):
        with self.lock:

            amp += random.randint(-5, 5)
            speed += random.uniform(-0.03, 0.03)

            amp = max(5, min(85, amp))
            speed = max(0.05, speed)

            self.left.angle = amp
            self.right.angle = -amp

            time.sleep(speed)

            self.left.angle = -amp
            self.right.angle = amp

            time.sleep(speed)

    def _loop(self):
        while self.running:

            min_amp, max_amp, min_speed, max_speed = EMOTIONS[self.emotion]

            amp = random.randint(min_amp, max_amp)
            speed = random.uniform(min_speed, max_speed)

            self._move(amp, speed)

            time.sleep(random.uniform(0.05, 0.25))

    def stop(self):
        self.running = False

        self.thread.join()

        self.left.angle = 0
        self.right.angle = 0

        time.sleep(0.2)

        self.left.detach()
        self.right.detach()
