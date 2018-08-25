naturals = ["C", "D", "E", "F", "G", "A", "B"]
chromatic_sharps = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
chromatic_flats = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
chromatic_all = ["C", "C#", "Db", "D", "D#", "Eb", "E", "F", "F#", "Gb", "G", "G#", "Ab", "A", "A#", "Bb", "B"]
qualities = {
    "maj": [0, 4, 7], 
    "maj7": [0, 4, 7, 11], 
    "maj9": [0, 4, 7, 11, 2], 
    "min": [0, 3, 7],
    "dim": [0, 3, 6],
    "aug": [0, 4, 8],
    "sus2": [0, 2, 7],
    "sus4": [0, 5, 7],
    "sus2sus4": [0, 2, 5, 7],
}
extensions = {
    # name: (adds, removes); if int, just adds
    "7": 10,
    "(maj7)": 11,
    "b5": (6, 7),
    "#5": (8, 7),
    "add9": 2,
    "add6": 9,
    "add11": 7,
    "add13": 9,
    "#11": 6,
}

def match_substrings(string, subs):
    matched = []
    for sub in subs:
        if len(sub) > len(string):
            continue
        for i, char in enumerate(string):
            if i >= len(sub) or (i + 1 == len(string) and char == sub[i]):
                matched.append(sub)
                break
            elif char != sub[i]:
                break
    return matched

def parse_note_names(notes):
    out = []
    for note in notes:
        if "#" in note:
            out.append(chromatic_sharps.index(note))
        else:
            out.append(chromatic_flats.index(note))
    return out

def parse_chord_name(chord_str):
    """
    Convert user-inputted chord name into list of notes.
    """
    if not chord_str or chord_str[0] not in naturals:
        raise InvalidChordNameException()
    if len(chord_str) == 1:
        root = chromatic_sharps.index(chord_str)
        return transpose(qualities["maj"], root)
    root, quality, remove_tones, added_tones = (None, None, [], [])
    unmatched = len(chord_str)
    i = 0
    while i < len(chord_str):
        if root is None:
            if i > 1:
                raise InvalidChordNameException()
            candidates = chromatic_all.copy()
            matches = match_substrings(chord_str[i:], candidates)
            if not matches:
                raise InvalidChordNameException()
            root = max(matches, key=len)
            unmatched -= len(root)
            i += len(root)
            root = chromatic_flats.index(root) if "b" in root else chromatic_sharps.index(root)
            continue
        else:
            if quality is None:
                candidates = list(qualities.keys())
                matches = match_substrings(chord_str[i:], candidates)
                print(chord_str[i:], candidates, matches)
                quality = "maj" if not matches else max(matches, key=len)
                if matches:
                    unmatched -= len(quality)
                    i += len(quality)
                    continue
            candidates = list(extensions.keys())
            matches = match_substrings(chord_str[i:], candidates)
            if matches:
                ext = max(matches, key=len)
                if type(extensions[ext]) is tuple:
                    added_tones.append(extensions[ext][0])
                    remove_tones.append(extensions[ext][1])
                else:
                    added_tones.append(extensions[ext])
                unmatched -= len(ext)
                i += len(ext)
                continue
        # TODO: slash chords
        # TODO: refactor...maybe just use regex
        i += 1
    if unmatched > 0:
        raise InvalidChordNameException()
    quality = quality or "maj"
    chord = transpose(qualities[quality], root) + transpose(added_tones, root)
    for tone in remove_tones:
        chord.remove(tone)
    return chord

def transpose(notes, interval):
    return [(note + interval) % 12 for note in notes]

class InvalidChordNameException(Exception):
    pass
