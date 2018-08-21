from ..voicings.music import match_substrings, parse_chord_name, InvalidChordNameException
import pytest

def test_match_substrings():
    test_cases = [
        ("hello", ["h", "he", "l", "x"], ["h", "he"]),
        ("maj", ["m", "ma", "maj"], ["m", "ma", "maj"]),
        ("C", ["C#"], []),
    ]
    for (string, subs, matched) in test_cases:
        assert match_substrings(string, subs) == matched

class TestChordParsing:
    def test_invalid_names(self):
        invalid_names = [
            "",
            " ",
            "a",
            "x",
            "X",
            "Cma",
            "Cminor",
        ]
        for name in invalid_names:
            print(name)
            with pytest.raises(InvalidChordNameException):
                parse_chord_name(name)
    
    def test_chords(self):
        test_cases = [
            ("C", [0, 4, 7]), 
            ("Cmaj", [0, 4, 7]), 
            ("C#", [1, 5, 8]), 
            ("Db", [1, 5, 8]), 
            ("Cmin", [0, 3, 7]),
            ("Cdim", [0, 3, 6]),
            ("Caug", [0, 4, 8]),
            ("D#aug", [3, 7, 11]),
            ("Cmaj7", [0, 4, 7, 11]), 
            ("Cmaj9", [0, 4, 7, 11, 2]), 
            ("Csus2", [0, 2, 7]),
            ("Csus4", [0, 5, 7]),
            ("C7", [0, 4, 7, 10]),
            ("Cmin7", [0, 3, 7, 10]),
            ("Cmin7b5", [0, 3, 6, 10]),
            ("Cmaj7#11", [0, 4, 7, 11, 6]),
            ("Cmaj7#5", [0, 4, 8, 11]),
        ]
        for name, notes in test_cases:
            assert parse_chord_name(name) == notes
