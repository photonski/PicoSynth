import time
import board
import digitalio
import analogio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import audioio
import math
import adafruit_ssd1306

# Initialize the potentiometer inputs
attack_pot = analogio.AnalogIn(board.GP26)
decay_pot = analogio.AnalogIn(board.GP27)
sustain_pot = analogio.AnalogIn(board.GP28)
release_pot = analogio.AnalogIn(board.GP22)
pitch_pot = analogio.AnalogIn(board.GP21)
volume_pot = analogio.AnalogIn(board.GP20)

# Initialize the switches
play_continuous_switch = digitalio.DigitalInOut(board.GP2)
play_continuous_switch.direction = digitalio.Direction.INPUT
play_continuous_switch.pull = digitalio.Pull.UP

play_staccato_switch = digitalio.DigitalInOut(board.GP3)
play_staccato_switch.direction = digitalio.Direction.INPUT
play_staccato_switch.pull = digitalio.Pull.UP

# Initialize the keyboard
kbd = Keyboard(usb_hid.devices)

# Initialize the keyboard layout
layout = KeyboardLayoutUS(kbd)

# Define the modulation range
MODULATION_RANGE = 2000  # Adjust this based on your preference

# Define the note frequencies for the middle C scale
scale_frequencies = [
    261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88
]

# Define the keycodes for the keys QWERTYU
keycodes = [
    Keycode.Q, Keycode.W, Keycode.E, Keycode.R, Keycode.T, Keycode.Y, Keycode.U
]

# Define the audio sample rate and buffer size
SAMPLE_RATE = 22050  # Adjust this based on your preference
BUFFER_SIZE = 128

# Initialize the audio output
audio = audioio.AudioOut(board.GP0)

# Initialize the display
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
oled.mode = 1

# Define the display mode
DISPLAY_MODE_PAGE1 = 1
DISPLAY_MODE_PAGE2 = 2
display_mode = DISPLAY_MODE_PAGE1

# Function to map potentiometer values to modulation range
def map_pot_value(value):
    return int((value / 65535) * MODULATION_RANGE)

# Function to generate a sine wave sample
def generate_sample(frequency, volume):
    sample = bytearray(BUFFER_SIZE)
    for i in range(BUFFER_SIZE):
        value = int((math.sin(2 * math.pi * frequency * i / SAMPLE_RATE) + 1) * 32767 / 2)
        value = int(value * volume / MODULATION_RANGE)
        sample[i] = value & 0xFF
    return sample

# Function to update the display with the current parameters
def update_display(page):
    oled.fill(0)
    if page == DISPLAY_MODE_PAGE1:
        oled.text("Attack: " + str(attack_pot.value), 0, 0, 1)
        oled.text("Decay: " + str(decay_pot.value), 0, 10, 1)
        oled.text("Sustain: " + str(sustain_pot.value), 0, 20, 1)
    elif page == DISPLAY_MODE_PAGE2:
        oled.text("Release: " + str(release_pot.value), 0, 0, 1)
        oled.text("Pitch: " + str(pitch_pot.value), 0, 10, 1)
        oled.text("Volume: " + str(volume_pot.value), 0, 20, 1)
    oled.show()

# Function to play a note based on potentiometer values
def play_note():
    pitch = map_pot_value(pitch_pot.value)
    attack = map_pot_value(attack_pot.value)
    decay = map_pot_value(decay_pot.value)
    sustain = map_pot_value(sustain_pot.value)
    release = map_pot_value(release_pot.value)

    # Determine the note based on potentiometer values
    note_index = int(pitch / (65535 / len(scale_frequencies)))
    note_frequency = scale_frequencies[note_index]

    # Play the note with digital audio output
    keycode = keycodes[note_index]
    kbd.press(keycode)

    # Set the volume based on the potentiometer value
    volume = map_pot_value(volume_pot.value)

    # Generate the audio sample for the note
    sample = generate_sample(note_frequency, volume)

    # Play the audio sample
    with audioio.AudioOut(board.GP22) as audio:
        audio.play(audioio.RawSample(sample), loop=True)

        time.sleep(attack / 1000)
        kbd.release_all()
        time.sleep(decay / 1000)
        kbd.press(keycode)
        time.sleep(sustain / 1000)
        kbd.release_all()
        time.sleep(release / 1000)

    audio.stop()

# Main loop
while True:
    if not play_continuous_switch.value:
        play_note()

    if not play_staccato_switch.value:
        play_note()

    if display_mode == DISPLAY_MODE_PAGE1:
        update_display(DISPLAY_MODE_PAGE1)
        if not digitalio.DigitalInOut(board.GP21).value:
            display_mode = DISPLAY_MODE_PAGE2
    elif display_mode == DISPLAY_MODE_PAGE2:
        update_display(DISPLAY_MODE_PAGE2)
        if not digitalio.DigitalInOut(board.GP21).value:
            display_mode = DISPLAY_MODE_PAGE1

    time.sleep(0.1)  # Adjust sleep duration based on your preference
