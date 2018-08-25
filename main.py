import argparse
from voicings.music import parse_note_names
from voicings.voicings import voicings

parser = argparse.ArgumentParser(description="Find all voicings of a chord on a string instrument.")
parser.add_argument("chord", type=str, help="The name of the chord to query")
parser.add_argument("-f", type=int, help="The maximum number of fingers allowed")
parser.add_argument("-s", type=str, nargs="+", help="The tuning of the instrument")
parser.add_argument("-r", type=int, help="The string to use as the chord root")
args = parser.parse_args()

if __name__ == "__main__":
    # TODO: pass args properly into voicings.
    string_names = args.s or ["E", "A", "D", "G", "B", "E"]
    strings = parse_note_names(string_names)
    print(strings)
    root_string = args.r or 0
    fingers = args.f or 4
    query = voicings(args.chord, strings=strings, root_string=root_string, fingers=fingers)
    for i, result in enumerate(query):
        print("({} / {})".format(i+1, len(query)))
        for string, fret in zip(string_names, result.fretted):
            print("{}| {}".format(string, fret))
        print("\n")
