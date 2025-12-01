# YT Editor

## Steps for adding a new video

### Step 1 - Create a new `{videoNumber}` directory in [`videos`](videos)

1. **Create a `videos` subdirectory**:
    1. Download/create a video, remove black bars and save it as `full.mp4`
    2. Trim the full video to ~1 minute and save it as `short.mp4`
2. **Create an `audio` subdirectory**:
    1. **Create a `parts/{part}` subdirectory**:
        1. Download/create a piano arrangement and save it as `full.mid`
        2. Repeat for all parts
    2. Simplify the full midi files and convert them to json:
        ```bash
        python src/audio/simplify_midi.py {videoNumber} --parts {parts}
        python src/audio/midi2json.py {videoNumber} --parts {parts}
        ```
    3. Edit `simple.json`:
        - Set `"bpm"`, add initial rest and cut off notes to match the trimmed video
        - Split up notes/rests longer than 2.133 seconds
        - Add original language/translations to `"captionLabels"` and include lyrics, e.g.:
            ```json5
            {
                "captionLabels": [
                    // Original language and translation(s)
                    {"language": "fr", "name": "lyrics (original)"},
                    {"language": "en", "name": "lyrics (cover)"}
                ],
                "parts": [{"notes": [
                    // A note with translated lyrics
                    {"note": "C4", "ticks": 8, "lyrics": [
                        {"language": "fr", "text": "Bonjour"},
                        {"language": "en", "text": "Hello"}
                    ]}

                    // A note with untranslated lyrics
                    {"note": "C4", "ticks": 8, "lyrics": "Bob"}

                    // End previous lyrics early
                    {"note": null, "ticks": 8, "lyrics": null}
                ]}]
            }
            ```
    4. Encrypt the audio files:
        ```bash
        python src/encryption/encrypt.py videos/{videoNumber}/audio/**/*.mid \
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
    2. Repeat 11 times (8 times for black and white):
        <!--
        - maximum row counts:
            | Aspect ratio | Android (16:9) | iOS (16:9) | Windows (16:9 large text) | macOS (16:9) | macOS (native) | Windows (9:16 large text) | macOS (9:16) |
            |:-------------|----------------|-----------:|--------------------------:|-------------:|---------------:|--------------------------:|-------------:|
            | **4:3**      |         5 rows |    12 rows |                   33 rows |      49 rows |        63 rows |                 (61 rows) |      84 rows |
            | **3:2**      |            ??? |    12 rows |                   33 rows |      49 rows |        56 rows |                 (61 rows) |      84 rows |
            | **16:9**     |            ??? |    12 rows |                   33 rows |      47 rows |                |                   58 rows |      84 rows |
            | **64:27**    |            ??? |     9 rows |                   25 rows |      35 rows |        45 rows |                 (43 rows) |      65 rows |
        -->
        - 1 layer:
            | Aspect ratio |          Rows (16:9) | Rows (native) |   Rows (9:16) |
            |:-------------|---------------------:|--------------:|--------------:|
            | **4:3**      | 5, 12, 24, 36 and 48 |            60 |     72 and 84 |
            | **3:2**      | 5, 12, 24, 36 and 48 |               | 60, 72 and 84 |
            | **16:9**     | 5, 10, 20, 30 and 40 |               | 50, 60 and 70 |
            | **64:27**    |  4, 8, 16, 24 and 32 |            40 |     48 and 56 |
        - 4 layers (colored only):
            | Aspect ratio  |   Rows (16:9) |
            |:--------------|--------------:|
            | **4:3 / 3:2** | 30, 36 and 42 |
            | **16:9**      | 25, 30 and 35 |
            | **64:27**     | 20, 24 and 28 |
    3. Compress the Srv3 files:
        ```bash
        python src/compression/compress.py videos/{videoNumber}/resolutions/*.srv3
        ```
5. **Create a `thumbnails` subdirectory**:
    1. Download/create a thumbnail, crop it to 16:9 and save it as `original.png`
    2. Convert the original thumbnail to Srv3:
        ```bash
        mp4_to_srv3 videos/{videoNumber}/thumbnails/original.png --rows 84
        ```
    3. Upload the output Srv3 as a subtitle to any video in YouTube Studio
    4. Set character edge style to "raised", take a screenshot, crop it and save it as `ascii.png`
    5. Combine both thumbnails and save them as `combined.png`

### Step 2 - Add a new entry to `"videos"` in [`config/settings.json`](config/settings.json)

- Set `"videoNumber"` to `{videoNumber}`
- Set `"skipped"` to `false`
- Set `"title"` to `"{artist} - {name} - but it's subtitles"`
- Add lyrics/translations, timestamps and relevant links to `"descriptionLines"`
- Set `"thumbnailName"` to `"combined"`
- Add relevant playlist titles from https://www.youtube.com/@nicezombies1/playlists
- Add relevant tags
- Set `"categoryTitle"` to one of the categories from [`config/categories.json`](config/categories.json)
- If applicable, add title and year to `"gameInfo"`
- Set `"resolutionLanguage"` to `"en"`
- Add resolution names (with leading spaces)
