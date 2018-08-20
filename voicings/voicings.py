from collections import Counter
from .fingerings import Fingering

class QueryResult:
    def __init__(self, fingering, query_notes):
        self.rank = fingering.rank(notes=query_notes)
        self.fretted = fingering.fretted
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
