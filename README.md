# YT Editor

## Steps for adding a new video

### Step 1 - Create a new `{videoNumber}` directory in [`videos`](videos)

1. **Create a `videos` subdirectory**:
    1. Download/create a video and save it as `full.mp4`
    2. Trim the full video to ~1 minute and save it as `short.mp4`
2. **Create an `audio` subdirectory**:
    1. Download/create a piano arrangement and save it as `full.mid`
    2. Simplify the full midi and convert it to json:
        ```bash
        python src/audio/simplify_midi.py {videoNumber}
        python src/audio/midi2json.py {videoNumber}
        ```
    3. Edit `simple.json`:
        - Set `"bpm"`, add initial rest and cut off notes to match the trimmed video
        - Add original language/translations to `"captionLabels"` and include lyrics, e.g.:
            ```json5
            {
                "captionLabels": [
                    // Original language and translation(s)
                    {"language": "fr", "name": "lyrics (original)"},
                    {"language": "en", "name": "lyrics (cover)"}
                ],
                "notes": [
                    // A note with translated lyrics
                    {"note": "C4", "ticks": 8, "lyrics": [
                        {"language": "fr", "text": "Bonjour"},
                        {"language": "en", "text": "Hello"}
                    ]}

                    // A note with untranslated lyrics
                    {"note": "C4", "ticks": 8, "lyrics": "Bob"}

                    // End previous lyrics early
                    {"note": null, "ticks": 8, "lyrics": null}
                ]
            }
            ```
    4. Encrypt the audio files:
        ```bash
        python src/encryption/encrypt.py videos/{videoNumber}/audio/*.mid \
            videos/{videoNumber}/audio/*.json
        ```
3. **Generate srt files**:
    ```bash
    python src/audio/generate_captions.py {videoNumber}
    ```
4. **Generate srv3 files**:
    1. Convert the trimmed video to Srv3:
        ```bash
        cd videos/{videoNumber}
        mp4_to_srv3 videos/short.mp4 --subfile captions/{captionLanguages}.srt \
            --dir resolutions \
            --submsoffset 4000 --rows {rows} --layers {layers} --targetsize {targetsize}
        ```
    2. Repeat 12 times (8 times for black and white):
        - 1 layer:
            | Aspect ratio |  Rows (landscape) |   Rows (portrait) |
            |:-------------|------------------:|------------------:|
            | **4x3**      | 12, 24, 36 and 48 | 58, 68, 78 and 88 |
            | **16x9**     | 11, 22, 33 and 44 | 54, 64, 74 and 84 |
            | **64x27**    |  8, 16, 24 and 32 | 38, 44, 50 and 56 |
        - 4 layers (colored only):
            | Aspect ratio |  Rows (landscape) |
            |:-------------|------------------:|
            | **4x3**      | 30, 36, 42 and 48 |
            | **16x9**     | 28, 34, 40 and 46 |
            | **64x27**    | 20, 24, 28 and 32 |
    3. Compress the Srv3 files:
        ```bash
        python src/compression/compress.py videos/{videoNumber}/resolutions/*.srv3
        ```
5. **Create a `thumbnails` subdirectory**:
    1. Download/create a 16x9 thumbnail and save it as `original.png`
    2. Convert the original thumbnail to Srv3:
        ```bash
        mp4_to_srv3 videos/{videoNumber}/thumbnails/original.png --rows 84
        ```
    3. Upload the output Srv3 as a subtitle to any video in YouTube Studio
    4. Take a screenshot, crop it and save it as `ascii.png`

### Step 2 - Add a new entry to `"videos"` in [`config/settings.json`](config/settings.json)

- Set `"videoNumber"` to `{videoNumber}`
- Set `"title"` to `"{artist} - {name}"`
- Add lyrics/translations, timestamps and relevant links to `"descriptionLines"`
- Add relevant playlist titles from https://www.youtube.com/@nicezombies1/playlists
- Add relevant tags
- Set `"categoryTitle"` to one of the categories from [`config/categories.json`](config/categories.json)
- If applicable, add title and year to `"gameInfo"`
- Set `"resolutionLanguage"` to the original language
- Add resolution names (with leading spaces)
