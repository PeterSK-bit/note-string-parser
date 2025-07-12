import argparse
from string import ascii_letters, digits

def count_spaces_between_letters(note_string: str, start_index: int) -> int:
    """
    Count spaces between the current note and the next one in the string.
    Used to determine pause duration between notes.
    """

    for next_index in range(start_index + 1, len(note_string)):
        if note_string[next_index].isalpha():
            return note_string[start_index + 1:next_index].count(" ")
    return 0  # No second note found

def is_sharp_note(notes: str, index: int) -> bool:
    """
    Checks if the note at a given index is sharp.
    """

    return (index > 0 and notes[index - 1] == "^") or (index + 1 < len(notes) and notes[index + 1] == "#")

def get_frequency_pause(notes: str) -> tuple[list[int], list[float]]:
    """
    Converts a string of musical notes into a sequence of [frequency, pause_duration] pairs.
    Supports sharps (^A or A#), and pauses indicated by '-' after a note.
    """
    
    TONE_FREQUENCIES = {
        "A": 440,
        "B": 493,
        "C": 523,
        "D": 587,
        "E": 659,
        "F": 698,
        "G": 784,
    }

    result = []

    for i, char in enumerate(notes):
        if not char.isalpha():
            continue
        if char not in TONE_FREQUENCIES:
            continue  # Skip invalid notes like Z, H, etc.

        freq = round(TONE_FREQUENCIES[char] * 2 ** (1 / 12)) if is_sharp_note(notes, i) else TONE_FREQUENCIES[char]

        # Check for pause (dash) or calculate based on space
        if i + 1 < len(notes) and notes[i + 1] == "-":
            pause = 0
        else:
            spaces = count_spaces_between_letters(notes, i)
            pause = round(0.05 + spaces * 0.05, 2)

        result.append([freq, pause])

    return tuple(result)

def main():
    parser = argparse.ArgumentParser(description="Convert note string to frequency/pause sequence.")
    parser.add_argument("note_string", nargs="?", help="String of notes (optional)")
    parser.add_argument("--output", "-o", help="Name of the output .txt file (optional)")
    args = parser.parse_args()

    # Ask for note string if not provided as argument
    if not args.note_string:
        note_string = input("Enter your note string: ").strip()
    else:
        note_string = args.note_string

    sequence = get_frequency_pause(note_string)

    # Ask whether to write to file if --output was not used
    if args.output is None:
        choice = input("Do you want to save the output to a file? [y/N]: ").strip().lower()
        if choice == "y":
            output_file = input("Enter output file name: ").strip()

            # Sanitize filename
            safe_chars = ascii_letters + digits + "-_."
            output_file = "".join(c for c in output_file if c in safe_chars)
            if not output_file:
                print("INFO: Invalid filename. Using default name 'output.txt'")
                output_file = "output.txt"

            with open(output_file, "w") as f:
                for freq, pause in sequence:
                    f.write(f"{freq},{pause}\n")

            print(f"INFO: Output written to {output_file}")
        else:
            print("INFO: Output (console):")
            for freq, pause in sequence:
                print(f"{freq},{pause}")
    else:
        # If --output is used, sanitize and write directly
        safe_chars = ascii_letters + digits + "-_."
        output_file = "".join(c for c in args.output if c in safe_chars)
        if not output_file:
            print("INFO: Invalid filename. Using default name 'output.txt'")
            output_file = "output.txt"

        with open(output_file, "w") as f:
            for freq, pause in sequence:
                f.write(f"{freq},{pause}\n")

        print(f"INFO: Output written to {output_file}")

if __name__ == "__main__":
    main()