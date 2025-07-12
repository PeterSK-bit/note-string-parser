# Note String Parser for microcontroller buzzer

This Python script converts a custom string of musical notes into a list of frequency and pause duration pairs, designed specifically for use with microcontrollers like the ESP32.

The output is well-suited for buzzer playback using PWM or tone-generating libraries in MicroPython or similar environments.

---

## Features

- Parses a custom note format (e.g. `"B B ^C#-^D-B ^D ^E ^C#-B ^C#-B-A"`)
- Supports:
  - **Natural notes**: A, B, C, D, E, F, G
  - **Sharps**: using `^` before the letter or `#` after (e.g., `^C`, `C#`)
  - **Pauses/Sustain**: using `-` after a note to indicate a full stop
  - **Timing**: spaces between notes influence pause duration
- Returns a list of `[frequency, pause_duration]` pairs

---

## Example

```python
input: "B B ^C#-^D-B ^D ^E ^C#-B ^C#-B-A"
output: ([493, 0.1], [493, 0.1], [554, 0.05], [622, 0], [493, 0.1], [622, 0.1], [698, 0.1], [554, 0.05], [493, 0.1], [554, 0.05], [493, 0], [440, 0.05])
```

---

## How It Works

1. Iterates through each character in the string
2. When it finds a letter:
    - Looks for sharp indicators (^ or #)
    - Checks for - pause or calculates pause based on spaces
3. Adds a tuple to the result list: [frequency, pause_duration]

---

## Disclaimer
> I'm not a musician, just a hobbyist with an interest in electronics and coding.
> So, if some notes or timing seem off, it's totally possible.
> This was a fun experiment, and contributions or corrections are welcome.

---

## Use Cases

- ESP32, Arduino, Raspberry Pi buzzer playback
- Educational sound experiments
- Converting text-based music into timing instructions

### Target Use Case
Designed for use in MicroPython or Arduino projects, especially on the ESP32, where you want to play simple tunes using a buzzer.

---

## License
MIT License — use freely, modify as you wish.