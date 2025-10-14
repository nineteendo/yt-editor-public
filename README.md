# YT Editor

## Steps for adding a new video

1. **Create a new `{videoNumber}` directory in [`videos`](videos)**:
    1. **Create a `videos` subdirectory**:
        1. Download or create a video and save it as `full.mp4`
        2. Trim the full video to ~1 minute and save it as `short.mp4`
    2. **Create an `audio` subdirectory**:
        1. Download or create a piano arrangement and save it as `full.mid`
        2. Simplify the full midi and convert it to json:
            ```bash
            python src/audio/simplify_midi.py {videoNumber}
            python src/audio/midi2json.py {videoNumber}
            ```
        3. Edit `simple.json` to align with the trimmed video and include lyrics/translations
        4. Encrypt the audio files:
            ```bash
            python src/encryption/encrypt.py --glob videos/{videoNumber}/audio/*.mid
            python src/encryption/encrypt.py videos/{videoNumber}/audio/simple.json
            ```
    3. **Create a `thumbnails` subdirectory**:
        1. Download or create a thumbnail and save it as `original.png`
        2. Convert the original thumbnail to Srv3 using https://github.com/nineteendo/Mp4-To-Srv3:
            ```bash
            cd ../Mp4-To-Srv3
            python main.py ../yt-editor-public/videos/{videoNumber}/thumbnails/original.png {rows}
            ```
        3. Upload the output Srv3 as a subtitle to any video in YouTube Studio
        4. Take a screenshot and save it as `ascii.png`
2. **Add a new entry to `"videos"` in [`config/settings.json`](config/settings.json)**:
    1. Set `"videoNumber"` to `{videoNumber}`
    2. Set `"title"` to `"{artist} - {name}"`
    3. Add lyrics and relevant links to `"descriptionLines"`
    4. Add relevant tags
    5. Set `"categoryTitle"` to one of the categories from [`config/categories.json`](config/categories.json)
    6. (Add title and year to `"gameInfo"`)
    7. Add original language/translations to `"captionLabels"`
    8. Set `"resolutionLanguage"` to the original language
    9. Set `"bpm"` to match the trimmed video
    10. Set `"ppq"` to 16
3. **Finish the `{videoNumber}` directory in [`videos`](videos)**:
    1. **Generate captions**:
        <!--Depends on `"introDuration"`, `"captionLabels"`, `"bpm"` and `"ppq"`-->
        ```bash
        python generate_captions {videoNumber}
        ```
    2. **Create a `resolutions` subdirectory**:
        <!--Depends on `captions`-->
        1. Convert the trimmed video to Srv3 using https://github.com/nineteendo/Mp4-To-Srv3:
            ```bash
            cd ../Mp4-To-Srv3
            python main.py ../yt-editor-public/videos/{videoNumber}/videos/short.mp4 {rows} \
            --subfile ../yt-editor-public/videos/{videoNumber}/captions/{languages}.srt \
            --submsoffset 4
            ```
        2. Save the output Srv3 as `{height}p{fps}.srv3` and repeat 8 times.
4. **Finish the entry from `"videos"` in [`config/settings.json`](config/settings.json)**:
    1. Add resolutions to `"resolutionNames"`
        <!--Depends on `resolutions`-->
