from flask import Flask, render_template, request, jsonify
import RPi.GPIO as GPIO

app = Flask(__name__)

# GPIO 腳位設定
gpio_pins = [5, 6, 13, 16, 19, 20, 21, 26]
GPIO.setmode(GPIO.BCM)

try:  # The try block ensures cleanup even if errors occur
    # Set GPIO initial state to HIGH
    GPIO.setup(gpio_pins, GPIO.OUT)  # Setup inside the try block
    for pin in gpio_pins:
        GPIO.output(pin, GPIO.HIGH)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/toggle/<int:channel>', methods=['POST'])
    def toggle(channel):
        GPIO.output(gpio_pins[channel], not GPIO.input(gpio_pins[channel]))
        status = "ON" if GPIO.input(gpio_pins[channel]) == GPIO.LOW else "OFF"
        return jsonify({'status': status, 'channel': channel})

    if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0')

except KeyboardInterrupt:  # Handle Ctrl+C gracefully
    print("Exiting...")
except Exception as e: # Catch any other exceptions
    print(f"An error occurred: {e}")
finally:  # This block *always* runs
    GPIO.cleanup()  # Essential: Release GPIO pins
    print("GPIO cleaned up.") # Helpful message to confirm