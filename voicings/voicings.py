from .fingerings import Fingering
from collections import Counter

class QueryResult:
    def __init__(self, fingering, query_notes):
        self.rank = fingering.rank(notes=query_notes)
        self.complete = not any(fingering.note_counts[n] == 0 for n in query_notes)

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
