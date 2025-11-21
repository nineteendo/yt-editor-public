"""Convert midi to JSON."""
from __future__ import annotations

__all__: list[str] = []

from argparse import ArgumentParser, Namespace
from fractions import Fraction

import jsonyx as json
from mido import MidiFile, MidiTrack  # type: ignore

_BPM: float = 120
_INTRO_DURATION: int = 4
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
    parser.add_argument("--parts", type=int, default=1, help="Number of parts")
    return parser.parse_args()


def _midi_to_note_string(midi_note: int) -> str:
    octave, base_note = divmod(midi_note - 12, 12)
    return f"{_NOTE_NAMES[base_note]}{octave}"


def _convert_track(track: MidiTrack, ticks_per_beat: int) -> str:
    total_duration: Fraction = Fraction()
    notes: list[str] = []
    for msg in track:
        if duration := Fraction(_PPQ * msg.time, ticks_per_beat):
            old_total_duration: Fraction = total_duration
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

            if notes:
                notes.append(",\n")
                if not old_total_duration % (4 * _PPQ):
                    notes.append("\n")

            division: int = duration.denominator
            notes.append(8 * " ")
            notes.append(json.dumps({
                "note": note_str,
                "ticks": duration.numerator,
                **({"division": division} if division > 1 else {})
            }, end=""))

    return "".join(notes)


def _main() -> None:
    args: Namespace = _parse_args()
    audio_dir: str = f'videos/{args.video_number}/audio'
    parts: list[MidiTrack] = []
    for i in range(args.parts):
        midi: MidiFile = MidiFile(f'{audio_dir}/parts/{i + 1}/simple.mid')
        tracks: list[MidiTrack] = midi.tracks
        if len(tracks) != 1:
            raise SystemExit("Not exactly one track")

        parts.append(tracks[0])

    json_filename: str = f'{audio_dir}/simple.json'
    with open(json_filename, "w", encoding="utf-8") as fp:
        fp.write("\n".join([
            '{',
            f'    "introDuration": {_INTRO_DURATION},',
            '    "captionLabels": [],',
            '    "parts": ['
            + ', '.join("\n".join([
                f'{{"bpm": {_BPM}, "ppq": {_PPQ}, "notes": [',
                _convert_track(part, midi.ticks_per_beat),
                '    ]}'
            ]) for part in parts) + ']',
            '}',
        ]))


if __name__ == "__main__":
    _main()
