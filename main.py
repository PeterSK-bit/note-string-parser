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
    note_string = input("Insert notes: ")
    sequence = get_frequency_pause(note_string)
    print(sequence)

if __name__ == "__main__":
    main()
