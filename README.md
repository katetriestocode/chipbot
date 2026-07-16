# SnarkyShark
<img width="650" height="auto" alt="Untitled" src="https://github.com/user-attachments/assets/ce3288b8-70e0-44d6-bedf-920709c8bced" /><img width="250" height="auto" alt="Adobe Express - IMG_0402" src="https://github.com/user-attachments/assets/25bb90de-0de5-495e-b2fc-5cbbf746de43" />

A blahaj plushy that makes snarky jokes, powered by an LLM!

Our project is made for outpost, hackclub hackathon ending at open sauce!
It features:
1. proximity sensor
2. microphone
3. speakers
4. gyroscope
5. camera
6. hat (new!)

## Execute the code
### Install the requirements
```bash
pip install -r requirements.txt
```
or
```bash
python3 -m pip install -r requirements.txt
```

### Environment Variables
```ENV
ELEVEN_API_KEY = ""
ELEVEN_VOICE_ID = ""

GEMINI_API_KEY = ""
GEMINI_MODEL = "gemini-flash-latest"
GEMINI_TIMEOUT_MS = 10000

SERIAL_PORT = "/dev/tty.usbserial-<INSERT_PORT>"

```

### Run the code
From the computer:
```bash
python3 main_pc.py
```

From the Raspberry Pi Zero 2W:
```bash
python3 main_pi.py
```

### SSH Connection with the Raspberry Pi Zero 2W
```bash
ssh snarkyshark@snarkyshark.local
```
