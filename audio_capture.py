import soundcard as sc
import numpy as np
import sys

class AudioCapture:
    def __init__(self, device_index=None):
        self.rate = 16000
        self.channels = 1
        self.chunk = 4096
        self.mic = None
        self.is_recording = False
        
    def list_devices(self):
        print("\n--- Available Audio Input Devices ---")
        for m in sc.all_microphones(include_loopback=True):
            print(f"[] {m.name}")
        print("-------------------------------------\n")

    def start(self):
        print("Auto-detecting CABLE Output using SoundCard...")
        target_mic = None
        for m in sc.all_microphones(include_loopback=True):
            if 'cable output' in m.name.lower() and not m.isloopback:
                target_mic = m
                break
        
        if target_mic is None:
            print("Fallback: Using default microphone.")
            target_mic = sc.default_microphone()
            
        print(f"Targeting Audio Device: {target_mic.name}")
        
        try:
            self.mic = target_mic.recorder(samplerate=self.rate, channels=self.channels)
            self.is_recording = True
            print("Audio capture started successfully via modern WASAPI.")
        except Exception as e:
            print(f"Failed to start SoundCard audio capture: {e}")
            sys.exit(1)

    def generator(self):
        if not self.mic:
            return
            
        with self.mic as source:
            while self.is_recording:
                try:
                    # SoundCard returns numpy array of floats [-1.0, 1.0] shape (frames, channels)
                    data = source.record(numframes=self.chunk)
                    if len(data) > 0:
                        # Deepgram linear16 expects 16-bit integer PCM, so convert float to int16
                        int16_data = (data * 32767).astype(np.int16).tobytes()
                        yield int16_data
                except Exception as e:
                    pass

    def stop(self):
        self.is_recording = False

if __name__ == "__main__":
    ac = AudioCapture()
    ac.list_devices()
