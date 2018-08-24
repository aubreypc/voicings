from flask import Flask, request, jsonify
from .voicings.music import parse_note_names
from .voicings.voicings import voicings # TODO: sort out this spaghetti naming

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({})

@app.route("/voicings/<chord_name>/")
def query_voicings(chord_name):
    args = request.args
    string_names= args.get("strings", default="E,A,D,G,B,E").split(",")
    strings = parse_note_names(string_names)
    root_string_name = args.get("root_string", default=string_names[0], type=str)
    root_string = string_names.index(root_string_name)
    fingers = args.get("fingers", default=4, type=int)
    res = {
        "chord": chord_name,
        "strings": string_names,
        "root_string": root_string_name,
        "voicings": []
    }
    for query in voicings(chord_name, strings=strings, root_string=root_string, fingers=fingers):
        res["voicings"].append(query.fretted)
    return jsonify(res)
