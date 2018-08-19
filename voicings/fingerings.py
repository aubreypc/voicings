from collections import Counter

class Fingering:
    """
    A hand position on the fretboard.
    """
    def __init__(self, strings=[4, 9, 2, 7, 11, 4], fretted=None, fingers=4):
        self.strings = strings
        self.fingers = fingers if len(strings) >= fingers else len(strings)
        self.fretted = fretted or [None] * len(strings)
        self.validate()
 
    def validate(self):
        """
        Try to map fingers to fretted notes to ensure the fingering is physically possible to play.
        """
        self.counter = Counter(self.fretted)
        if len(self.counter.keys()) > self.fingers:
            raise ImpossibleFingerPositionException("Not enough fingers to fret/barre all notes.")
        pairs = [(i, fret) for i, fret in enumerate(self.fretted) if fret is not None]
        pairs.sort(key=(lambda p: p[1])) # sort (string, fret) pairs by fret
        if pairs[-1][1] - pairs[0][1] > 5:
            raise ImpossibleFingerPositionException("Leftmost and rightmost fret too far apart.")
        for string, fret in pairs:
            pass


class ImpossibleFingerPositionException(Exception):
    pass


class FingeringsGenerator:
    """
    Generator class for finding all fingerings which don't require unrealistic finger flexibility
    """
    def __init__(self, strings=[4, 9, 2, 7, 11, 4], fingers=4):
        self.strings = strings
        self.fingers = fingers if len(strings) >= fingers else len(strings)

    def generate(self, notes, root_string=0, mute_above=True):
        """
        Convert reachable_chord_tones output to Fingering objects, and yield those which validate.
        """
        # TODO
        pass

    def reachable_chord_tones(self, notes, root_string=0, mute_above=True):
        """
        Fix a chord's root note on a particular string, and return the chord tones close to that
        fret on all the other strings.
        """
        assert len(notes) >= 1
        reachable = [None] * len(self.strings)
        root_fret = (notes[0] - self.strings[root_string]) % 12
        reachable[root_string] = [root_fret]
        for i, string in enumerate(self.strings):
            if i == root_string or mute_above and i < root_string:
                reachable[i] = [] if not reachable[i] else reachable[i]
                continue
            stretch = 3 # TODO: determine this dynamically
            fret_range = list(range(root_fret - stretch, root_fret + stretch))
            if root_fret - stretch > 0:
                fret_range.insert(0, 0)
            reachable[i] = [fret for fret in fret_range if (string + fret) % 12 in notes]
        return reachable
