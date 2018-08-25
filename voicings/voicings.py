from collections import Counter
from .fingerings import FingeringsGenerator
from .music import parse_chord_name

class QueryResult:
    def __init__(self, fingering, query_notes):
        self.rank = fingering.rank(notes=query_notes)
        self.fretted = fingering.fretted.copy()
        note_count = fingering.note_count(notes=query_notes)
        self.complete = not any(note_count[n] == 0 for n in query_notes)

    def __lt__(self, other):
        return (self.complete, self.rank) < (other.complete, other.rank)

    def __le__(self, other):
        return (self.complete, self.rank) <= (other.complete, other.rank)

    def __gt__(self, other):
        return (self.complete, self.rank) > (other.complete, other.rank)

    def __ge__(self, other):
        return (self.complete, self.rank) >= (other.complete, other.rank)

    def __eq__(self, other):
        return (self.complete, self.rank) == (other.complete, other.rank)

    def __ne__(self, other):
        return (self.complete, self.rank) != (other.complete, other.rank)


def voicings(chord_str, strings=(4, 9, 2, 7, 11, 4), fingers=4, root_string=0, mute_above=False):
    """
    Fetch all of a chord's voicings and yield them in sorted order.
    """
    gen = FingeringsGenerator(strings=strings, fingers=fingers)
    chord = parse_chord_name(chord_str)
    res = []
    for voicing in gen.generate(chord, root_string=root_string, mute_above=mute_above):
        q = QueryResult(voicing, chord)
        res.append(q)
    res.sort()
    return res
