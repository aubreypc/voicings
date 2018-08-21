import argparse
from voicings.voicings import voicings

parser = argparse.ArgumentParser(description="Find all voicings of a chord on a string instrument.")
parser.add_argument("chord", type=str, help="The name of the chord to query")
parser.add_argument("-f", type=int, nargs=1, help="The maximum number of fingers allowed")
parser.add_argument("-s", type=str, nargs="+", help="The tuning of the instrument")
parser.add_argument("-r", type=int, nargs=1, help="The string to use as the chord root")
args = parser.parse_args()

if __name__ == "__main__":
    # TODO: pass args properly into voicings.
    strings = args.s if args.s else ["E", "A", "D", "G", "B", "E"]
    query = voicings(args.chord)
    for i, result in enumerate(query):
        print("({} / {})".format(i+1, len(query)))
        for string, fret in zip(strings, result.fretted):
            print("{}| {}".format(string, fret))
        print("\n")
