# AutoRobloxRantShorts

NOT PRODUCTION READY AT ALL, DON'T USE THIS LOL


### Todo

* remove hardcoded imagemagick path
* Linux support (bat -> sh, forward slashes)
* why do they need to be base64 encoded?
* put the temporary generated files in a folder instead of main directory
* autoclose windows when done
* autodetect number mismatch
* implement config
* auto detect "Running on local URL"

# How to Use

1. git clone this
2. Look at SETUP\_WINDOWS.md for windows or SETUP\_LINUX.md for linux
3. record your gameplay and save it as input.mkv in the main directory
4. place required assets
5. run run\_no\_console.vbs for windows, or "" for linux

## Required Assets

Place all of them in the assets directory

### spritesheet.txt

A 640x160 base64-encoded image with four 160x160 pictograms representing the emojis 😐, 🥀, 🙏, and 😭 respectively. Make your own or use a set like OpenMoji.

### font.txt

The font that will be used for subtitles. A base64-encoded TTF file I think? TikTok Sans for example.

### nah script.txt

The script that will be used as a style guide for the script generator. It should have bolded words in Markdown format.

### bgm.mp3

The background music for the video.

### vineboom.wav

The sound effect that will be played at the end of impactful sentences.

### thirteen.mp3

The voice source that will be used for text to speech. Note that f5-tts only uses the first ~10 seconds.

### confusing.png, depressing.png, positive.png, and shocking.png

The images that will flash if add_images is enabled in the config.

## Generating a Video

1. Replace "Why do we all have that one friend who..." with your topic
2. Click Generate All
3. Check the text on the top right. If it says "Good," you can most likely continue.
4. If the text is three numbers that don't match, use one or both of the other two Regenerate buttons until the second and third numbers match the first number. You can also edit the text by hand if you prefer.
5. Click "Start TTS Server." Wait until it says "Running on local URL" and then click "Generate TTS." todo: do this automatically
6. Click "View File." Listen to the generated audio file. f5-tts struggles with hyphens (it inserts a long pause like an em dash) and exclamation points (the pitch of the voice raises unnaturally). If this is an issue, edit the second textbox and regenerate the TTS with the previous two buttons.
7. Click Make Video.
8. Click Open Result.
9. If everything looks good, click Clean Up. If the subtitles don't line up, look more closely at the three textboxes. Make sure they all have the same words and have newlines in the same places. If something went wrong with the video, you only need to click Make Video again. (Sometimes Firefox decides to randomly not work)

## Tips

* Don't use the script generator. It's terrible. Until I improve it, I recommend generating the script with a better model like ChatGPT and using the Regenerate buttons to generate the other scripts.
