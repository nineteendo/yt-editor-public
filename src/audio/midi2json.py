"""Convert midi to JSON."""
from __future__ import annotations

__all__: list[str] = []

from argparse import ArgumentParser, Namespace
from contextlib import redirect_stdout
from fractions import Fraction

import jsonyx as json
from mido import MidiFile, MidiTrack  # type: ignore

_NOTE_NAMES: list[str] = [
    'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B'
]
_PPQ: int = 16


def _parse_args() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        description="Convert midi to JSON."
    )
    parser.add_argument(
        "video_number", type=int, help="The video number to process"
    )
    return parser.parse_args()


def _midi_to_note_string(midi_note: int) -> str:
    octave, base_note = divmod(midi_note - 12, 12)
    return f"{_NOTE_NAMES[base_note]}{octave}"


def _convert_track(track: MidiTrack, ticks_per_beat: int) -> None:
    total_duration: Fraction = Fraction()
    first: bool = True
    print("[")
    for msg in track:
        if duration := Fraction(_PPQ * msg.time, ticks_per_beat):
            if not first:
                print(",")

            if total_duration and not total_duration % (4 * _PPQ):
                print()

            total_duration += duration
            if msg.type == 'note_on' and msg.velocity:
                note_str: str | None = None
            elif (
                msg.type == 'note_on' and not msg.velocity
                or msg.type == 'note_off'
            ):
                note_str = _midi_to_note_string(msg.note)
            else:
                continue

            first = False
            division: int = duration.denominator
            print(end=4 * " ")
            json.dump({
                "note": note_str,
                "ticks": duration.numerator,
                **({"division": division} if division > 1 else {})
            }, end="")

    print()
    print(end="]")


def _main() -> None:
    video_number: int = _parse_args().video_number
    midi: MidiFile = MidiFile(f'videos/{video_number}/audio/simple.mid')
    tracks: list[MidiTrack] = midi.tracks
    if len(tracks) != 1:
        raise ValueError("Not exactly one track")

    json_filename: str = f'videos/{video_number}/audio/simple.json'
    with open(json_filename, 'w', encoding='utf-8') as fp, redirect_stdout(fp):
        _convert_track(tracks[0], midi.ticks_per_beat)


if __name__ == "__main__":
    _main()
