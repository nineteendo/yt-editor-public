# YT Editor

## Steps for adding a new video

1. **Create a `{videoNumber}` directory in [`videos`](videos)**:
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
    3. **Generate captions**:
        ```bash
        python generate_captions {videoNumber}
        ```
    4. **Create a `resolutions` subdirectory**:
        1. Convert the trimmed video to Srv3 using https://github.com/nineteendo/Mp4-To-Srv3:
            ```bash
            cd ../Mp4-To-Srv3
            python main.py ../yt-editor-public/videos/{videoNumber}/videos/short.mp4 {rows} \
            --subfile ../yt-editor-public/videos/{videoNumber}/captions/{languages}.srt \
            --submsoffset 4
            ```
        2. Save the output Srv3 as `{height}p{fps}.srv3` and repeat 8 times.
    5. **Create a `thumbnails` subdirectory**:
        1. Download or create a thumbnail and save it as `original.png`
        2. Convert the original thumbnail to Srv3 using https://github.com/nineteendo/Mp4-To-Srv3:
            ```bash
            cd ../Mp4-To-Srv3
            python main.py ../yt-editor-public/videos/{videoNumber}/thumbnails/original.png {rows}
            ```
        3. Upload the output Srv3 as a subtitle to a video in YouTube Studio
        4. Take a screenshot and save it as `ascii.png`
2. **Update [`config/settings.json`](config/settings.json)**:
    <!--TODO: Add instructions-->
