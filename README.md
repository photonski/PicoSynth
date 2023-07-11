# **CURRENT BUILD NOT FUNCTIONAL - WORK IN PROGRESS**

# PicoSynth
Synthesizer on Pi Pico (RP2040) - CircuitPython

Install circuitpython onto your device and then just copy over the code.py file & merge the lib folder.
This was made specifically for the Raspberry Pi Pico (rp2040)

**Necessary Connections:**

    Connect the potentiometers:
        Connect the attack potentiometer's middle pin to GP26 on the Raspberry Pi Pico. Connect one of its outer pins to 3.3V, and the other outer pin to GND.
        Connect the decay potentiometer in the same way, with its middle pin connected to GP27.
        Connect the sustain potentiometer in the same way, with its middle pin connected to GP28.
        Connect the release potentiometer in the same way, with its middle pin connected to GP22.
        Connect the volume potentiometer in the same way, with its middle pin connected to GP21.

    Connect the switches:
        Connect one side of the play_continuous switch to GP2, and the other side to GND.
        Connect one side of the play_staccato switch to GP3, and the other side to GND.
        Connect one side of the shift button to GP20, and the other side to GND.

    Connect the SSD1306 display:
        Connect the display's SDA pin to GP8 on the Raspberry Pi Pico.
        Connect the display's SCL pin to GP9 on the Pico.
        Connect the display's VCC pin to 3.3V.
        Connect the display's GND pin to GND.

    Connect the audio output:
        Connect a speaker or audio amplifier to the GP0 pin on the Raspberry Pi Pico.
        
Make sure you have the necessary components, such as potentiometers, switches, SSD1306 display module, and speaker or audio amplifier, to establish the connections.

Once you have made these connections, you can upload the code to your Raspberry Pi Pico running CircuitPython, and your digital instrument should be ready to use with the display showing the parameter values.

**How It Works**

1. **Importing Libraries and Initializing Components:**
   - The necessary libraries and modules are imported at the beginning of the code, including `board`, `digitalio`, `analogio`, `usb_hid`, `adafruit_hid.keyboard`, `adafruit_hid.keycode`, `adafruit_hid.keyboard_layout_us`, `audioio`, and `math`.
   - The potentiometers, switches, keyboard, keyboard layout, audio output, and SSD1306 display are initialized with their respective pins and configurations.

2. **Defining Constants and Variables:**
   - The code defines constants and variables for the modulation range, note frequencies, keycodes, sample rate, and buffer size.
   - The display mode is defined as page 1 initially.

3. **Mapping Potentiometer Values and Generating Audio Samples:**
   - The `map_pot_value()` function is defined to map the potentiometer values to the modulation range.
   - The `generate_sample()` function is defined to generate a sine wave audio sample based on the note frequency and volume. The sample is calculated using the math library and stored in a bytearray.

4. **Updating the Display:**
   - The `update_display()` function is defined to update the SSD1306 display with the current parameter values.
   - The display is cleared, and depending on the display mode (page 1 or page 2), the relevant parameter values are displayed.

5. **Playing a Note:**
   - The `play_note()` function is defined to play a note based on the potentiometer values.
   - The function reads the potentiometer values, determines the note frequency, and plays the note using the keyboard HID module and digital audio output.
   - The volume is adjusted based on the potentiometer value.
   - The audio sample is generated and played through the audio output using the `audioio` module. The note is played with the specified attack, decay, sustain, and release times.

6. **Main Loop:**
   - The main loop continuously checks the state of the switches.
   - If the play_continuous switch is pressed, a note is played continuously.
   - If the play_staccato switch is pressed, a staccato note is played.
   - The display is updated with the current parameter values based on the display mode.
   - The loop sleeps for a short duration to avoid excessive CPU usage.

With this code, the potentiometers and switches allow you to control the parameters and trigger notes from the C major scale. The audio output produces digital audio through PWM, and the SSD1306 display shows the current parameter values. The code combines HID keyboard functionality, audio generation, and display updates to create a digital instrument using the Raspberry Pi Pico.

By adjusting the potentiometer values and pressing the switches, you can explore different musical sounds and melodies. The display provides real-time feedback on the current settings, making it easier to experiment and fine-tune the instrument.
