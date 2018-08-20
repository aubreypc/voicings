from collections import Counter

class Fingering:
    """
    A hand position on the fretboard.
    """
    def __init__(self, strings=(4, 9, 2, 7, 11, 4), fretted=None, fingers=4):
        self.strings = strings
        self.fingers = fingers if len(strings) >= fingers else len(strings)
        self.fretted = fretted or [None] * len(strings)
        self.validate()

    def __iter__(self):
        return iter(self.fretted)

    def validate(self):
        """
        Try to map fingers to fretted notes to ensure the fingering is physically possible to play.
        """
        # TODO: refactor to reduce awkward positions (especially partial barres)
        self.fret_counter = Counter(self.fretted)
        if len(self.fret_counter.keys()) > self.fingers:
            raise ImpossibleFingerPositionException("Not enough fingers to fret/barre all notes.")
        pairs = [(i, fret) for i, fret in enumerate(self.fretted) if fret is not None]
        pairs.sort(key=(lambda p: p[1])) # sort (string, fret) pairs by fret
        if pairs[-1][1] - pairs[0][1] > 5:
            raise ImpossibleFingerPositionException("Leftmost and rightmost fret too far apart.")

    def rank(self, notes=[]):
        """
        Count the occurrences of each chord tone in the fretted position, and assemble a tuple
        which can rank Fingering objects. Tuples can be stably sorted to arrange Fingerings by
        occurrences of the higher-priority (lower index) notes.
        """
        note_counts = self.note_count(notes=notes)
        return tuple(note_counts[note] for note in notes)

    def note_count(self, notes=[]):
        """
        Compare expected notes to actual notes.
        """
        played = [(st + fr) % 12 for st, fr in zip(self.strings, self.fretted) if fr is not None] 
        return Counter(played)


class ImpossibleFingerPositionException(Exception):
    pass


class FingeringsGenerator:
    """
    Generator class for finding all fingerings which don't require unrealistic finger flexibility
    """
    def __init__(self, strings=(4, 9, 2, 7, 11, 4), fingers=4):
        self.strings = strings
        self.fingers = fingers if len(strings) >= fingers else len(strings)

    def generate(self, notes, root_string=0, mute_above=True):
        """
        Using depth-first search, convert reachable_chord_tones output to Fingering objects,
        and yield those which validate.
        """
        depth = 0
        stack = []
        reachable = self.reachable_chord_tones(notes, root_string=root_string, mute_above=mute_above)
        reachable_init = [[fret for fret in reach] for reach in reachable]
        while True:
            if depth > len(self.strings) - 1:
                depth -= 1
                try:
                    f = Fingering(strings=self.strings, fretted=stack)
                    yield f
                except ImpossibleFingerPositionException:
                    pass
                stack.pop()
                continue
            if not reachable[depth]:
                if depth == 0:
                    break
                reachable[depth][:] = reachable_init[depth]
                depth -= 1
                stack.pop()
                continue
            stack.append(reachable[depth].pop())
            depth += 1

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
            reachable[i] = [] if not reachable[i] else reachable[i]
            if i == root_string or mute_above and i < root_string:
                continue
            stretch = 3
            fret_range = list(range(root_fret - stretch, root_fret + stretch))
            if root_fret - stretch > 0:
                fret_range.insert(0, 0)
            for note in notes: # Note index indicates voicing priority
                fret = (note - string) % 12
                if root_fret - stretch <= fret and fret <= root_fret + stretch:
                    reachable[i].append(fret)
        return reachable
