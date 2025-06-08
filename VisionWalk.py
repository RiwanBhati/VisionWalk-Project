import RPi.GPIO as GPIO
import time
import math
import requests # Import the requests library

# --- ThingSpeak Configuration ---
# !!! REPLACE THESE WITH YOUR ACTUAL THINGSPEAK DETAILS !!!
THINGSPEAK_CHANNEL_ID = '2951072' # Your ThingSpeak Channel ID (the number)
THINGSPEAK_WRITE_API_KEY = '7TRNV3V7I41P5HSF' # Your ThingSpeak Write API Key

# ThingSpeak API endpoint for updating a channel
THINGSPEAK_API_URL = f'https://api.thingspeak.com/update'

# Define which field number in ThingSpeak will store the distance
THINGSPEAK_DISTANCE_FIELD = 'field1'

# How often to send data to ThingSpeak (ThingSpeak free accounts limit is typically 15 seconds)
THINGSPEAK_SEND_INTERVAL_SEC = 20 # Set slightly higher than the limit to be safe
# --- End ThingSpeak Configuration ---


# --- Pin Configuration ---
TRIG = 23   # GPIO pin for the ultrasonic sensor's TRIG
ECHO = 24   # GPIO pin for the ultrasonic sensor's ECHO
BUZZER_PIN = 27 # GPIO pin for the buzzer's positive terminal

# --- Distance and Beep Configuration ---
MAX_DISTANCE_FOR_BEEP = 50  # Distance threshold in cm. Buzzer active if distance < this value.
MIN_DELAY_MS = 50           # Minimum delay between beeps in milliseconds (for closest distances)
MAX_DELAY_MS = 500          # Maximum delay between beeps in milliseconds (for distances near MAX_DISTANCE_FOR_BEEP)

MIN_DELAY_SEC = MIN_DELAY_MS / 1000.0
MAX_DELAY_SEC = MAX_DELAY_MS / 1000.0

# --- GPIO Setup ---
GPIO.setmode(GPIO.BCM) # Use BCM GPIO numbers

# Setup ultrasonic pins
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Setup buzzer pin
GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.LOW) # Initialize buzzer to OFF


# --- Function to get distance from ultrasonic sensor ---
def get_distance():
    # Send pulse
    GPIO.output(TRIG, True)
    time.sleep(0.00001) # 10 microseconds pulse
    GPIO.output(TRIG, False)

    # Wait for echo start
    pulse_start = time.time()
    timeout_start = time.time()
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if time.time() - timeout_start > 0.1: # Timeout after 100ms
            return -1 # Indicate error or no object detected

    # Wait for echo end
    pulse_end = time.time()
    timeout_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if time.time() - timeout_start > 0.1: # Timeout after 100ms
            return -1 # Indicate error

    # Calculate duration and distance
    duration = pulse_end - pulse_start
    distance = (duration * 34300) / 2

    # Return distance, rounded to 2 decimal places for cleaner data
    return round(distance, 2)

# --- Function to calculate beep delay based on distance ---
def calculate_beep_delay(distance_cm):
    clamped_distance = max(0, min(distance_cm, MAX_DISTANCE_FOR_BEEP))
    # Linear mapping: as distance goes 0 -> 50, delay goes MIN -> MAX
    delay = MIN_DELAY_SEC + (clamped_distance / MAX_DISTANCE_FOR_BEEP) * (MAX_DELAY_SEC - MIN_DELAY_SEC)
    # Ensure the delay stays within bounds
    return max(MIN_DELAY_SEC, min(delay, MAX_DELAY_SEC))


# --- Main Loop ---
last_send_time = 0 # Variable to track the last time data was sent to ThingSpeak

try:
    print("\n--- Starting Ultrasonic Distance & Buzzer Alert with ThingSpeak ---")
    print(f"Buzzer active if distance < {MAX_DISTANCE_FOR_BEEP} cm. Speed changes with distance.")
    print(f"Sending data to ThingSpeak Channel ID: {THINGSPEAK_CHANNEL_ID} every {THINGSPEAK_SEND_INTERVAL_SEC} seconds.")
    print("Press Ctrl+C to stop.")

    # Give sensor a moment to settle
    GPIO.output(TRIG, False)
    time.sleep(2)

    while True:
        current_time = time.time()
        dist = get_distance()

        if dist != -1: # If distance reading was successful
            print(f"Distance: {dist:.2f} cm    ", end='\r') # end='\r' overwrites the line

            # --- Send distance to ThingSpeak (if enough time has passed) ---
            if current_time - last_send_time >= THINGSPEAK_SEND_INTERVAL_SEC:
                try:
                    # Create the payload (data to send)
                    # This is a dictionary where keys are API parameters
                    payload = {
                        'api_key': THINGSPEAK_WRITE_API_KEY,
                        THINGSPEAK_DISTANCE_FIELD: dist # Using the field name defined
                    }
                    # Send a GET request to the ThingSpeak API
                    response = requests.get(THINGSPEAK_API_URL, params=payload, timeout=5) # 5 sec timeout

                    # Check the response status code (200 indicates success, returns the entry number)
                    if response.status_code == 200:
                        print(f"Distance: {dist:.2f} cm | Sent to ThingSpeak (Entry: {response.text})", end='\r')
                        last_send_time = current_time # Update last send time ONLY on success
                    else:
                        print(f"Distance: {dist:.2f} cm | ThingSpeak API Error: Status Code {response.status_code}", end='\r')

                except requests.exceptions.RequestException as e:
                    print(f"Distance: {dist:.2f} cm | ThingSpeak Send Error: {e}     ", end='\r')
                except Exception as e:
                     print(f"Distance: {dist:.2f} cm | Unexpected Send Error: {e}     ", end='\r')
            # --- End ThingSpeak Send ---


            if dist < MAX_DISTANCE_FOR_BEEP:
                # Calculate beep delay based on distance
                beep_delay = calculate_beep_delay(dist)

                # Make the buzzer beep (ON/OFF cycle)
                GPIO.output(BUZZER_PIN, GPIO.HIGH) # Buzzer ON
                time.sleep(beep_delay / 2.0)           # Beep ON for half the calculated delay

                GPIO.output(BUZZER_PIN, GPIO.LOW)  # Buzzer OFF
                time.sleep(beep_delay / 2.0)           # Stay OFF for the other half of the calculated delay

            else:
                # Distance is >= MAX_DISTANCE_FOR_BEEP, ensure buzzer is off
                GPIO.output(BUZZER_PIN, GPIO.LOW)
                # Add a small delay so we don't read too fast when far away and not sending data
                # This also prevents a tight loop when ThingSpeak sending is skipped
                time.sleep(0.1)

        else: # If distance reading failed (timeout)
             print("Distance: Reading Error      ", end='\r') # Indicate error
             GPIO.output(BUZZER_PIN, GPIO.LOW) # Ensure buzzer is off on error
             time.sleep(0.1) # Wait before trying again


except KeyboardInterrupt:
    print("\nStopped by user")

except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")


finally:
    # Ensure GPIO settings are cleaned up gracefully
    GPIO.cleanup()
    print("GPIO cleanup complete.")