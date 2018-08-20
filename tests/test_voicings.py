from ..voicings.fingerings import Fingering, FingeringsGenerator
from ..voicings.voicings import QueryResult
import pytest

class TestQueryResult:
    def test_comparisons(self): 
        compares = {
            ">": (lambda x, y: x > y),
            ">=": (lambda x, y: x >= y),
            "<": (lambda x, y: x < y),
            "<=": (lambda x, y: x <= y),
            "==": (lambda x, y: x == y),
            "!=": (lambda x, y: x != y)
        }
        test_cases = [
            # Equality checking
            ([4,9,2], [7,11,2], [3,2,0], [3,2,0], ["==", "<=", ">="]),
            # G maj triad vs. fifthless triad
            ([4,9,2], [7,11,2], [3,2,0], [3,2,5], [">",  ">=", "!="]),
        ]
        for (strings, notes, fretted1, fretted2, ops) in test_cases:
            f1 = Fingering(strings=strings, fretted=fretted1)
            f2 = Fingering(strings=strings, fretted=fretted2)
            q1 = QueryResult(f1, notes)
            q2 = QueryResult(f2, notes)
            for op in compares.keys():
                if op in ops:
                    print("{} {} {}?".format(fretted1, op, fretted2))
                    assert compares[op](q1, q2)
                else:
                    print("{} NOT {} {}?".format(fretted1, op, fretted2))
                    assert not compares[op](q1, q2)
