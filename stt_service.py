import os
from dotenv import load_dotenv
from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
)

class STTService:
    def __init__(self, on_transcript_callback):
        load_dotenv()
        self.api_key = os.getenv("DEEPGRAM_API_KEY")
        if not self.api_key:
            raise ValueError("DEEPGRAM_API_KEY not found in environment.")
            
        self.dg_client = DeepgramClient(self.api_key)
        self.dg_connection = self.dg_client.listen.live.v("1")
        self.on_transcript_callback = on_transcript_callback

        def on_message(client, result, **kwargs):
            if result is None:
                return
            
            # DEBUG: Print the raw result to understand the SDK structure
            # print(f"Raw Deepgram Result: {result}")
            
            # Deepgram returns a 'channel' object containing 'alternatives'
            # Check if there are valid results
            if not getattr(result, 'channel', None) or not result.channel.alternatives:
                return

            sentence = result.channel.alternatives[0].transcript
            if len(sentence) == 0:
                return
            
            is_final = result.is_final
            self.on_transcript_callback(sentence, is_final=is_final)

        def on_error(client, error, **kwargs):
            print(f"Deepgram Error: {error}")

        self.dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        self.dg_connection.on(LiveTranscriptionEvents.Error, on_error)

    def start(self):
        options = LiveOptions(
            model="nova-2",
            language="en-US",
            smart_format=True,
            encoding="linear16",
            channels=1,
            sample_rate=16000,
            interim_results=True,
            endpointing=100
        )
        # Attempt to connect to Deepgram's live streaming API
        if not self.dg_connection.start(options):
            print("Failed to start Deepgram connection")
            return
            
        print("Deepgram STT connection started successfully.")

    def send_audio(self, data):
        self.dg_connection.send(data)

    def stop(self):
        self.dg_connection.finish()
