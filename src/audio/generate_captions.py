"""Generate captions for a video."""
from __future__ import annotations

__all__: list[str] = []

from argparse import ArgumentParser, Namespace
from math import ceil, floor
from os import makedirs
from typing import Any

import jsonyx as json


def _parse_args() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        description="Generate captions for a video."
    )
    parser.add_argument(
        "video_number", type=int, help="The video number to process"
    )
    return parser.parse_args()


def _format_ms(ms: int) -> str:
    ss, ttt = divmod(ms, 1000)
    mm, ss = divmod(ss, 60)
    hh, mm = divmod(mm, 60)
    return f"{hh:02}:{mm:02}:{ss:02},{ttt:03}"


def _get_lyrics_text(lyrics: list[dict[str, Any]], language: str) -> str:
    for lyrics_translation in lyrics:
        if lyrics_translation["language"] == language:
            return lyrics_translation["text"]

    raise SystemExit(f"Could not find {language} in {lyrics}")


def _append_caption(
    captions: list[str],
    start: float,
    end: float,
    lyrics: list[dict[str, Any]] | str,
    languages: list[str]
) -> None:
    start_str: str = _format_ms(ceil(1000 * start))
    end_str: str = _format_ms(floor(1000 * end))
    if isinstance(lyrics, str):
        lyrics_text: str = lyrics
    else:
        lyrics_text = "\n".join(
            _get_lyrics_text(lyrics, language) for language in languages
        )

    captions.append("\n".join([
        f"{len(captions) + 1}",
        f"{start_str} --> {end_str}",
        lyrics_text
    ]))


def _get_captions(
    notes: list[dict[str, Any]],
    ticks_per_minute: float,
    end: float,
    languages: list[str]
) -> str:
    captions: list[str] = []
    start: float = 0
    lyrics: list[dict[str, Any]] | str | None = None
    for msg in notes:
        tick_count: int = msg["ticks"] / msg.get("division", 1)
        if "lyrics" in msg:
            new_lyrics: list[dict[str, Any]] | str | None = msg["lyrics"]
            if lyrics is not None:
                _append_caption(captions, start, end, lyrics, languages)

            lyrics = new_lyrics
            start = end

        end += 60 * tick_count / ticks_per_minute

    if lyrics is not None:
        _append_caption(captions, start, end, lyrics, languages)

    if not captions:
        raise SystemExit("Empty captions")

    return "\n\n".join(captions)


def _main() -> None:
    video_number: int = _parse_args().video_number
    audio_filename: str = f"videos/{video_number}/audio/simple.json"
    with open(audio_filename, "r", encoding="utf-8") as fp:
        audio: dict[str, Any] = json.load(fp)

    ticks_per_minute: float = audio["bpm"] * audio["ppq"]
    languages: list[str] = [
        caption_label["language"]
        for caption_label in audio["captionLabels"]
    ]
    caption_dir: str = f"videos/{video_number}/captions"
    makedirs(caption_dir, exist_ok=True)
    for language in languages:
        captions: str = _get_captions(
            audio["notes"], ticks_per_minute, audio["introDuration"],
            [language]
        )
        output_file: str = f"{caption_dir}/{language}.srt"
        with open(output_file, 'w', encoding="utf-8") as fp:
            fp.write(captions)

    if len(languages) >= 2:
        captions = _get_captions(
            audio["notes"], ticks_per_minute, audio["introDuration"],
            languages
        )
        output_file = f"{caption_dir}/{'-'.join(languages)}.srt"
        with open(output_file, 'w', encoding="utf-8") as fp:
            fp.write(captions)


if __name__ == "__main__":
    _main()
