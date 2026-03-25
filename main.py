import threading
import time
import keyboard
from ui import StealthUI
from audio_capture import AudioCapture
from stt_service import STTService
from llm_service import LLMService

class Application:
    def __init__(self):
        self.llm = LLMService()
        self.silence_timeout = 5.0 # Increased default from 3s to 5s to address user's feedback
        
        def save_settings(prompt, timeout):
            self.llm.update_system_instruction(prompt)
            self.silence_timeout = timeout
            
        self.ui = StealthUI(
            initial_prompt=self.llm.system_instruction,
            initial_timeout=self.silence_timeout,
            on_settings_save_callback=save_settings
        )
        self.audio = AudioCapture()
        
        # Buffer to hold transcribed speech until the interviewer stops
        self.current_thought = ""
        self.last_final_time = time.time()
        self.is_paused = False
        self.is_generating_response = False

        self.stt = STTService(on_transcript_callback=self.handle_transcript)

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.ui.update_question("[PAUSED - Gizli Mod] F9 to resume...")
            self.ui.hide_window()
        else:
            self.ui.show_window()
            self.ui.update_question("[RESUMED - Dinleniyor...]")
            self.current_thought = ""

    def handle_transcript(self, transcript, is_final):
        """Callback fired by STTService on new interim or final transcripts."""
        if is_final:
            self.current_thought += transcript + " "
            self.ui.update_question(self.current_thought)
            self.last_final_time = time.time()
        else:
            # Display interim changes alongside what has already been finalized
            self.ui.update_question(self.current_thought + transcript)

    def check_for_silence(self):
        """Monitors timestamps. If no speech is detected for X seconds, request LLM response."""
        while True:
            time.sleep(0.5)
            # If silence_timeout seconds have passed since the last final transcript, treat it as a question
            if self.current_thought.strip() and (time.time() - self.last_final_time > self.silence_timeout):
                if self.is_generating_response:
                    continue # Wait until the current generation is finished before triggering another
                    
                self.is_generating_response = True
                question_to_ask = self.current_thought.strip()
                # Reset right away so we can transcribe the next question
                self.current_thought = "" 
                
                # Fetch Answer from Gemini asynchronously
                def fetch():
                    try:
                        accumulated_answer = ""
                        # Let the UI know we finished the question block
                        self.ui.finish_question()
                        self.ui.update_suggestion("Generating response...", is_loading=True)
                        
                        for chunk_text in self.llm.generate_suggestion_stream(question_to_ask):
                            accumulated_answer += chunk_text
                            self.ui.update_suggestion(accumulated_answer, is_loading=True)
                            
                        # Finalize the bubble once stream completes
                        self.ui.update_suggestion(accumulated_answer, is_loading=False)
                    except Exception as e:
                        print(f"Fetch Error: {e}")
                    finally:
                        self.is_generating_response = False
                
                threading.Thread(target=fetch, daemon=True).start()

    def process_audio(self):
        """Orchestrates pulling from audio and pushing to STT."""
        try:
            self.stt.start()
            self.audio.start()
            
            for audio_chunk in self.audio.generator():
                if not self.is_paused:
                    self.stt.send_audio(audio_chunk)
                
        except KeyboardInterrupt:
            self.audio.stop()
            self.stt.stop()

    def start(self):
        # Register global hotkey
        keyboard.add_hotkey('f9', self.toggle_pause)

        # 1. Start silence checker loop
        threading.Thread(target=self.check_for_silence, daemon=True).start()
        
        # 2. Start audio pipeline thread
        threading.Thread(target=self.process_audio, daemon=True).start()
        
        print("Application backend started. Launching Stealth UI...")
        # 3. Block on Tkinter mainloop
        self.ui.start()

if __name__ == "__main__":
    app = Application()
    app.start()
