import threading
import time
import pigpio
import random

LEFT_SERVO = 12
RIGHT_SERVO = 13

CENTER = 1500

EMOTIONS = {
    "HAPPY": (220, 280, 0.16, 0.22),
    "EXCITED": (420, 500, 0.08, 0.12),
    "CURIOUS": (150, 220, 0.30, 0.40),
    "THINKING": (90, 150, 0.50, 0.70),
    "CONFUSED": (300, 380, 0.20, 0.30),
    "SLEEPY": (60, 100, 0.70, 0.90),
    "THANKFUL": (180, 240, 0.22, 0.30),
    "NEUTRAL": (120, 180, 0.40, 0.55),
}

class ServoMotors:
    def __init__(self):
        self.pi = pigpio.pi()

        if not self.pi.connected:
            raise RuntimeError("pigpiod is not running")
        
        self.lock = threading.Lock()

        self.emotion = "NEUTRAL"
        self.running = True

        self.pi.set_servo_pulsewidth(LEFT_SERVO, CENTER)
        self.pi.set_servo_pulsewidth(RIGHT_SERVO, CENTER)

        self.thread = threading.Thread(
            target=self._loop,
            daemon=True
        )

        self.thread.start()
    
    def react(self):
        with self.lock:
            self.pi.set_servo_pulsewidth(LEFT_SERVO, CENTER + 80)
            self.pi.set_servo_pulsewidth(RIGHT_SERVO, CENTER - 80)

            time.sleep(0.08)

            self.pi.set_servo_pulsewidth(LEFT_SERVO, CENTER)
            self.pi.set_servo_pulsewidth(RIGHT_SERVO, CENTER)

    def set_emotion(self, emotion):
        emotion = emotion.upper()

        if emotion not in EMOTIONS:
            emotion = "NEUTRAL"

        self.emotion = emotion

    def _move(self, amp, speed):
        with self.lock:
            amp += random.randint(-30, 30)
            speed += random.uniform(-0.03, 0.03)

            speed = max(0.05, speed)

            left = max(500, min(2500, CENTER + amp))
            right = max(500, min(2500, CENTER - amp))

            self.pi.set_servo_pulsewidth(
                LEFT_SERVO,
                left
            )

            self.pi.set_servo_pulsewidth(
                RIGHT_SERVO,
                right
            )

            time.sleep(speed)

            left = max(500, min(2500, CENTER - amp))
            right = max(500, min(2500, CENTER + amp))

            self.pi.set_servo_pulsewidth(
                LEFT_SERVO,
                left
            )

            self.pi.set_servo_pulsewidth(
                RIGHT_SERVO,
                right
            )

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

        self.pi.set_servo_pulsewidth(LEFT_SERVO, 0)
        self.pi.set_servo_pulsewidth(RIGHT_SERVO, 0)

        self.pi.stop()
