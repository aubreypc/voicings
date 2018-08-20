from ..voicings.fingerings import Fingering, FingeringsGenerator, ImpossibleFingerPositionException
import pytest

class TestFingering:
    def test_validate(self):
        fail_kwargs = [
            # Not enough fingers:
            {"strings": [4,9,2], "fretted": [3,2,5], "fingers": 0},
            {"strings": [4,9,2], "fretted": [3,2,5], "fingers": 1},
            {"strings": [4,9,2], "fretted": [3,2,5], "fingers": 2},

            # Not enough strings:
            {"strings": [], "fretted": [1]},
            {"strings": [1], "fretted": [1,2]},

            # Too far of a stretch:
            {"strings": [1,2], "fretted": [1, 10]},
            
        ]
        for kwargs in fail_kwargs:
            with pytest.raises(ImpossibleFingerPositionException):
                print(kwargs)
                Fingering(**kwargs)

    def test_assign_rank(self):
        test_cases = [
            # Major triad, root position
            {"strings": [4,9,2], "fretted": [3,2,0], "notes": [7,11,2], "rank": (1,1,1)},
            # Missing the fifth
            {"strings": [4,9,2], "fretted": [3,2,5], "notes": [7,11,2], "rank": (2,1,0)},
            # Missing the third
            {"strings": [4,9,2], "fretted": [3,5,0], "notes": [7,11,2], "rank": (1,0,2)},
        ]
        for kwargs in test_cases:
            expected = kwargs.pop("rank")
            notes = kwargs.pop("notes")
            assert Fingering(**kwargs).rank(notes=notes) == expected

    def test_compare_rank(self):
        # TODO: this should actually go in test_voicings, with QueryResult
        pass

class TestFingeringsGenerator:
    def test_reachable_chord_tones(self):
        test_cases = [
            # (strings, notes, excepted output) pairs
            # Be careful: test case output should be in order,
            # with fret index matching note index.
            ([4, 9, 2], [7, 11, 2], [[3], [2,5], [5,0]]), 
            ([0,0], [0,1], [[0], [0,1]]),
            ([0,0], [1,0], [[1], [1,0]]),
        ]
        for (strings, notes, output) in test_cases:
            fg = FingeringsGenerator(strings=strings)
            assert fg.reachable_chord_tones(notes=notes) == output
