# AutoRobloxRantShorts

NOT PRODUCTION READY AT ALL, DON'T USE THIS LOL

* todo: remove hardcoded file paths
  todo: why do they need to be base64 encoded?
  todo: put the temporary generated files in a folder instead of main directory
  todo: autoclose windows when done
  todo: add "Subscribe." to first textbox so numbers match
  todo: autodetect number mismatch
* in align\_subtitles.sh
* imagemagick binary

# How to Use

1. git clone this
2. Look at SETUP\_WINDOWS.md for windows or SETUP\_LINUX.md for linux
3. record your gameplay and save it as input.mkv in the AutoRobloxRantShorts directory
4. place required assets
5. run run\_no\_console.vbs for windows, or "" for linux

## Required Assets

Place all of them in the assets directory

### spritesheet.txt

A 640x160 base64-encoded image with four 160x160 pictograms representing the emojis 😐, 🥀, 🙏, and 😭 respectively. Make your own or use a set like OpenMoji.

### font.txt

The font that will be used for subtitles. A base64-encoded TTF file I think? TikTok Sans for example.

### nah script.txt

The script that will be used as a style guide for the script generator. It should have bolded words.

### bg.mp3

The background music for the video.

### vineboom.wav

The sound effect that will be played at the end of impactful sentences.

### thirteen.mp3

The voice source that will be used for text to speech. Note that f5-tts only uses the first ~10 seconds.

## Generating a Video

1. Replace "Why do we all have that one friend who..." with your topic
2. Click Generate All
3. Check the three textboxes and the the three numbers in the top right. All three numbers should match. (todo: add "Subscribe." to first text so this is actually true)
4. If the numbers don't match, use one or both of the other two Regenerate buttons until the second and third numbers match. (The first number isn't really important) You can also edit the text by hand if you prefer.
5. Click "Start TTS Server." Wait until it says "Running on local URL" and then click "Generate TTS." todo: do this automatically
6. Click "View File." Listen to the generated audio file. f5-tts struggles with hyphens and exclamation points. If this is an issue, edit the second textbox and regenerate the TTS with the previous two buttons.
7. Click Align Subtitles. todo: combine add subtitles and render video and add "view final video" button
8. Click Render Video.
9. Check the video "FINALVIDEO.mp4"
10. If everything looks good, click Clean Up.

## Tips

* Don't use the script generator. It's terrible. Until I improve it, I recommend generating the script with a better model like ChatGPT and using the Regenerate buttons to generate the other scripts.
