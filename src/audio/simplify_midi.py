"""Simplify midi file."""
from __future__ import annotations

__all__: list[str] = []

from argparse import ArgumentParser, Namespace

from mido import Message, MidiFile, MidiTrack  # type: ignore


def _parse_args() -> Namespace:
    parser: ArgumentParser = ArgumentParser(description="Simplify midi file.")
    parser.add_argument(
        "video_number", type=int, help="The video number to process"
    )
    return parser.parse_args()


def _event_key(event: tuple[int, Message]) -> tuple[int, bool]:
    abs_time, msg = event
    return abs_time, msg.type == 'note_on' and msg.velocity


def _merge_tracks(tracks: list[MidiTrack]) -> MidiTrack:
    events: list[tuple[int, Message]] = []
    for track in tracks:
        abs_time: int = 0
        for msg in track:
            abs_time += msg.time
            events.append((abs_time, msg))

    new_track: MidiTrack = MidiTrack()
    last_time: int = 0
    for abs_time, msg in sorted(events, key=_event_key):
        new_track.append(msg.copy(time=abs_time - last_time))
        last_time = abs_time

    return new_track


def _simplify_track(track: MidiTrack) -> MidiTrack:
    new_track: MidiTrack = MidiTrack()
    current_msg: Message | None = None
    current_time: int = 0
    for msg in track:
        current_time += msg.time
        if (
            msg.type == 'note_off'
            or msg.type == 'note_on' and not msg.velocity
        ):
            if current_msg is not None and msg.note == current_msg.note:
                if current_time:
                    new_track.append(current_msg)
                    new_track.append(
                        Message('note_off', note=msg.note, time=current_time)
                    )
                    current_time = 0
                else:
                    current_time += current_msg.time

                current_msg = None
        elif msg.type == 'note_on' and msg.velocity:
            if current_msg is None:
                current_msg = Message(
                    'note_on', note=msg.note, time=current_time
                )
                current_time = 0
            elif msg.note > current_msg.note:
                if current_time:
                    new_track.append(current_msg)
                    new_track.append(Message(
                        'note_off', note=current_msg.note, time=current_time
                    ))
                    current_time = 0
                    current_msg = Message('note_on', note=msg.note, time=0)
                else:
                    current_msg = Message(
                        'note_on', note=msg.note, time=current_msg.time
                    )

    return new_track


def _main() -> None:
    video_number: int = _parse_args().video_number
    midi: MidiFile = MidiFile(f'videos/{video_number}/audio/full.mid')
    new_midi: MidiFile = MidiFile()
    new_midi.tracks.append(_simplify_track(_merge_tracks(midi.tracks)))
    new_midi.save(f'videos/{video_number}/audio/simple.mid')


if __name__ == "__main__":
    _main()
