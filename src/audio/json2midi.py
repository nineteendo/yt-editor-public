"""Convert JSON to midi."""
from __future__ import annotations

__all__: list[str] = []

import re
from argparse import ArgumentParser, Namespace
from re import DOTALL, MULTILINE, VERBOSE, Pattern, RegexFlag
from typing import Any

import jsonyx as json
from mido import Message, MidiFile, MidiTrack  # type: ignore

_BASE_NOTES: dict[str, int] = {
    "C": 0,
    "D": 2,
    "E": 4,
    "F": 5,
    "G": 7,
    "A": 9,
    "B": 11
}
_FLAGS: RegexFlag = VERBOSE | MULTILINE | DOTALL
_NOTE_STRING: Pattern = re.compile(r"([A-G])([#b]?)([2-6])", _FLAGS)


def _parse_args() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        description="Generate captions for a video."
    )
    parser.add_argument(
        "video_number", type=int, help="The video number to process"
    )
    return parser.parse_args()


def _note_string_to_midi(note_str: str) -> int:
    if not (match := _NOTE_STRING.fullmatch(note_str)):
        raise ValueError(f"Invalid note string: {note_str}")

    note_name, accidental, octave = match.groups()
    midi: int = 12 * (int(octave) + 1) + _BASE_NOTES[note_name]
    if accidental == '#':
        midi += 1
    elif accidental == 'b':
        midi -= 1

    return midi


def _main() -> None:
    video_number: int = _parse_args().video_number
    audio_filename: str = f"videos/{video_number}/audio/simple.json"
    with open(audio_filename, "r", encoding="utf-8") as fp:
        audio: dict[str, Any] = json.load(fp)

    midi: MidiFile = MidiFile()
    track: MidiTrack = MidiTrack()
    current_time: int = 0
    for msg in audio["notes"]:
        time: int = midi.ticks_per_beat * msg["ticks"] // audio["ppq"]
        if (note_str := msg["note"]) is not None:
            note: int = _note_string_to_midi(note_str)
            track.append(Message('note_on', note=note, time=current_time))
            current_time = 0
            track.append(Message('note_off', note=note, time=time))
        elif track:
            current_time += time

    midi.tracks.append(track)
    midi.save(f'videos/{video_number}/audio/simple.mid')


if __name__ == "__main__":
    _main()
