import tkinter as tk
from tkinter import messagebox
import time
try:
    import RPi.GPIO as GPIO
    HARDWARE_AVAILABLE = True
except ImportError:
    HARDWARE_AVAILABLE = False

# Banner
BANNER = """
**********************************************
*       HandyLight Control 2025              *
* Coded by Pakistani Ethical Hacker          *
*         Mr. Sabaz Ali Khan                 *
*                                            *
* A secure and efficient light control system *
**********************************************
"""

# Configuration
LED_PIN = 18  # Example GPIO pin for Raspberry Pi
BRIGHTNESS_STEP = 10  # PWM brightness increment

class HandyLightControl:
    def __init__(self, root):
        self.root = root
        self.root.title("HandyLight Control 2025")
        self.root.geometry("400x300")
        self.is_light_on = False
        self.brightness = 0
        self.pwm = None

        # Initialize hardware if available
        if HARDWARE_AVAILABLE:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(LED_PIN, GPIO.OUT)
            self.pwm = GPIO.PWM(LED_PIN, 100)  # 100 Hz frequency
            self.pwm.start(0)  # Start PWM at 0% duty cycle
        else:
            print("Hardware not detected. Running in simulation mode.")

        # Print banner
        print(BANNER)

        # GUI Elements
        tk.Label(root, text="HandyLight Control 2025", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(root, text="Coded by Mr. Sabaz Ali Khan", font=("Arial", 10)).pack()

        # Control Frame
        control_frame = tk.Frame(root)
        control_frame.pack(pady=20)

        # On/Off Button
        self.toggle_button = tk.Button(control_frame, text="Turn On", command=self.toggle_light, width=15)
        self.toggle_button.grid(row=0, column=0, padx=10)

        # Brightness Slider
        tk.Label(control_frame, text="Brightness").grid(row=1, column=0, pady=10)
        self.brightness_slider = tk.Scale(control_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_brightness)
        self.brightness_slider.grid(row=2, column=0)

        # Status Label
        self.status_label = tk.Label(root, text="Light: OFF | Brightness: 0%", font=("Arial", 12))
        self.status_label.pack(pady=20)

        # Exit Button
        tk.Button(root, text="Exit", command=self.exit_program, width=15).pack(pady=10)

    def toggle_light(self):
        self.is_light_on = not self.is_light_on
        if self.is_light_on:
            self.toggle_button.config(text="Turn Off")
            self.brightness = 50  # Default brightness when turning on
            self.brightness_slider.set(self.brightness)
            self.update_brightness(self.brightness)
        else:
            self.toggle_button.config(text="Turn On")
            self.brightness = 0
            self.brightness_slider.set(0)
            self.update_brightness(0)
        self.update_status()

    def update_brightness(self, value):
        self.brightness = int(value)
        if HARDWARE_AVAILABLE and self.is_light_on:
            self.pwm.ChangeDutyCycle(self.brightness)
        self.update_status()

    def update_status(self):
        status = f"Light: {'ON' if self.is_light_on else 'OFF'} | Brightness: {self.brightness}%"
        self.status_label.config(text=status)

    def exit_program(self):
        if messagebox.askokcancel("Exit", "Do you want to exit HandyLight Control?"):
            if HARDWARE_AVAILABLE:
                self.pwm.stop()
                GPIO.cleanup()
            self.root.destroy()

def main():
    root = tk.Tk()
    app = HandyLightControl(root)
    root.mainloop()

if __name__ == "__main__":
    main()