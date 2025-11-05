# External Dependencies
---
Tested on Python 3.11.9 and pip 21.2.
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

## Install PyTorch
NVIDIA GPU
```
# Install pytorch with your CUDA version, e.g.
pip install torch==2.4.0+cu124 torchaudio==2.4.0+cu124 --extra-index-url https://download.pytorch.org/whl/cu124
```
AMD GPU
```
# Install pytorch with your ROCm version (Linux only), e.g.
pip install torch==2.5.1+rocm6.2 torchaudio==2.5.1+rocm6.2 --extra-index-url https://download.pytorch.org/whl/rocm6.2
```
Intel GPU
```
# Install pytorch with your XPU version, e.g.
# Intel® Deep Learning Essentials or Intel® oneAPI Base Toolkit must be installed
pip install torch torchaudio --index-url https://download.pytorch.org/whl/test/xpu

# Intel GPU support is also available through IPEX (Intel® Extension for PyTorch)
# IPEX does not require the Intel® Deep Learning Essentials or Intel® oneAPI Base Toolkit
# See: https://pytorch-extension.intel.com/installation?request=platform
```
Apple Silicon
```
# Install the stable pytorch, e.g.
pip install torch torchaudio
```
# WSL Instructions
Start menu -> search "Turn Windows features on and off" -> Turn on "Windows Subsystem for Linux"
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



