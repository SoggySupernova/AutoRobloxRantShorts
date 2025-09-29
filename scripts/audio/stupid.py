print("Loading...")
print("Don't close the window when it says 'loaded as API', it's not done yet!")
from gradio_client import Client, handle_file

client = Client("http://localhost:7860/")

with open('finalsub.txt','r') as txt:
  tx = txt.read()

print('Generating...')
print("Please don't close this window.")

result = client.predict(
  ref_audio_input=handle_file('assets/thirteen.mp3'),
  ref_text_input="",
  gen_text_input=tx,
  remove_silence=False,
  randomize_seed=True,
  seed_input=0,
  cross_fade_duration_slider=0.15,
  nfe_slider=32,
  speed_slider=1,
  api_name="/basic_tts"
)

with open(result[0],'rb') as la:
  with open('audio.wav','wb') as file:
    file.write(la.read())
    print('Finished. You may now close both windows.')
print(result[0])