# External Dependencies
---
Tested on Python 3.11.9.
---
You need ffmpeg, ollama, ImageMagick, and firefox correctly installed and configured. You need to download the `mistral` model as well:
```shell
ollama pull mistral
```
Also, because windows is stupid sometimes, you need to enable WSL.


Install libraries:
```
pip install -r requirements.txt
```

# Common Errors because pip is dumb
Or maybe I'm dumb?

## ModuleNotFoundError: No module named 'packaging'

Solution:
```
python -m pip install --upgrade packaging
```

## ModuleNotFoundError: No module named 'librosa'

```
python -m pip install --upgrade librosa
```

## Install Torch for Nvidia GPU
```
pip install torch==2.4.0+cu124 torchaudio==2.4.0+cu124 --extra-index-url https://download.pytorch.org/whl/cu124
```
## More errors yay!
```
pip install --force-reinstall -v "numpy==1.26.4"
```

# WSL Instructions
```bash
wsl --install
cd ~
sudo apt update
sudo apt upgrade -y
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev espeak libespeak-dev ffmpeg
wget https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz
tar -xvf Python-3.10.0.tgz
cd Python-3.10.0
./configure --enable-optimizations
make
sudo make altinstall
python3.10 -m venv venv
source venv/bin/activate
pip install numpy==1.22.4
pip install aeneas

```
