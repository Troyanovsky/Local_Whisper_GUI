# Local_Whisper_GUI: Whisper Transcriber
Whisper Transcriber is a simple GUI application that allows you to transcribe audio files using the Faster-Whisper library.

## Installation
First, install the faster-whisper library with the following command:
```bash
pip install faster-whisper
```

## Usage
To run the application, execute the following command:
```bash
python3 app.py
```

This will launch the Whisper Transcriber GUI.
NOTE: it may take a while to download the model during the first time usage. Model used: Whisper Small.

1. Click the Choose File button to select an audio file from your local storage.  
2. Optionally, check the With Timestamp box if you want the transcription to include timestamps.  
3. Click the Start button to begin the transcription process.  
4. Once the transcription is complete, the results will be displayed in the text area, including the detected language and word count.  
