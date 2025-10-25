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
        1. Set `"bpm"`, add initial rest and cut off notes to match the trimmed video
        2. Add original language/translations to `"captionLabels"` and include lyrics, e.g.:
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
        python src/encryption/encrypt.py --glob videos/{videoNumber}/audio/*.mid
        python src/encryption/encrypt.py videos/{videoNumber}/audio/simple.json
        ```
3. **Generate srt files**:
    ```bash
    python src/audio/generate_captions.py {videoNumber}
    ```
4. **Create a `resolutions` subdirectory**:
    1. Convert the trimmed video to Srv3 using https://github.com/nineteendo/Mp4-To-Srv3:
        ```bash
        cd ../Mp4-To-Srv3
        python main.py ../yt-editor-public/videos/{videoNumber}/videos/short.mp4 {rows} \
            --layers {layers} \
            --subfile ../yt-editor-public/videos/{videoNumber}/captions/{languages}.srt \
            --submsoffset 4000
        ```
    2. Repeat 12 times.
    3. Compress the Srv3 files:
        ```bash
        python src/compression/compress.py --glob videos/{videoNumber}/resolutions/*.srv3
        ```
5. **Create a `thumbnails` subdirectory**:
    1. Download/create a thumbnail and save it as `original.png`
    2. Convert the original thumbnail to Srv3 using https://github.com/nineteendo/Mp4-To-Srv3:
        ```bash
        cd ../Mp4-To-Srv3
        python main.py ../yt-editor-public/videos/{videoNumber}/thumbnails/original.png {rows}
        ```
    3. Upload the output Srv3 as a subtitle to any video in YouTube Studio
    4. Take a screenshot and save it as `ascii.png`

### Step 2 - Add a new entry to `"videos"` in [`config/settings.json`](config/settings.json)

1. Set `"videoNumber"` to `{videoNumber}`
2. Set `"title"` to `"{artist} - {name}"`
3. Add lyrics/translations, timestamps and relevant links to `"descriptionLines"`
4. Add relevant tags
5. Set `"categoryTitle"` to one of the categories from [`config/categories.json`](config/categories.json)
6. If applicable, add title and year to `"gameInfo"`
7. Set `"resolutionLanguage"` to the original language
8. Add resolution names (with leading spaces)
