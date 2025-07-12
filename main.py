import argparse
from string import ascii_letters, digits
import json

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

    return result

def write_output(sequence, output_file, format):
    with open(output_file, "w") as f:
        if format == "python":
            f.write(str(sequence))
        elif format == "json":
            json.dump(sequence, f, indent=2)
        elif format == "csv":
            for freq, pause in sequence:
                f.write(f"{freq},{pause}\n")
        elif format == "cpp":
            f.write("std::vector<std::pair<int, float>> notes = {\n")
            for freq, pause in sequence:
                f.write(f"  {{{freq}, {pause}f}},\n")
            f.write("};\n")
        else:
            raise ValueError("Unsupported format")
        
def sanitize_file_name(name):
    safe_chars = ascii_letters + digits + "-_."
    output_file = "".join(c for c in name if c in safe_chars)

    if not output_file:
        print("INFO: Invalid filename. Using default name 'output.txt'")
        return "output.txt"
    
    return output_file

def main():
    parser = argparse.ArgumentParser(description="Convert note string to frequency/pause sequence.")
    parser.add_argument("note_string", nargs="?", help="String of notes (optional)")
    parser.add_argument( "--format", choices=["python", "json", "csv", "cpp"], default="python", help="Output format: python, json, csv, or cpp (default: python)")
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
            output_file = sanitize_file_name(output_file)

            try:
                write_output(sequence, output_file, args.format)
                print(f"INFO: Output written to {output_file} in {args.format} format")
            except ValueError as e:
                print(f"ERROR: {e}")

        else:
            print("INFO: Output (console):")
            if args.format == "python":
                print(sequence)
            elif args.format == "json":
                print(json.dumps(sequence, indent=2))
            elif args.format == "csv":
                for freq, pause in sequence:
                    print(f"{freq},{pause}")
            elif args.format == "cpp":
                print("std::vector<std::pair<int, float>> notes = {")
                for freq, pause in sequence:
                    print(f"  {{{freq}, {pause}f}},")
                print("};")
            else:
                raise ValueError("Unsupported format")

    else:
        # If --output is used, sanitize and write directly
        output_file = sanitize_file_name(args.output)

        try:
            write_output(sequence, output_file, args.format)
            print(f"INFO: Output written to {output_file} in {args.format} format")
        except ValueError as e:
            print(f"ERROR: {e}")


if __name__ == "__main__":
    main()