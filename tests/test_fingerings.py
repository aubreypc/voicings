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
            {"strings": [1,2], "fretted": [1, 10]}
        ]
        for kwargs in fail_kwargs:
            with pytest.raises(ImpossibleFingerPositionException):
                print(kwargs)
                Fingering(**kwargs)


class TestFingeringsGenerator:
    def test_fg(self):
        fg = FingeringsGenerator()
        print(fg.reachable_chord_tones([7, 11, 2]))
