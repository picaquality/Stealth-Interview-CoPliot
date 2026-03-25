import google.generativeai as genai
import os
from dotenv import load_dotenv

class LLMService:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment. Please define it in your .env file.")
        
        genai.configure(api_key=api_key)
        
        self.system_instruction = (
            "You are a helpful and concise AI assistant. "
            "Your goal is to provide short, relevant answers to the user's questions. "
            "Keep responses conversational and structured.\n"
            "Output Format: Provide the answer in 2-3 concise bullet points."
        )
        self._initialize_model()

    def _initialize_model(self):
        # Use generative model with current system instructions
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=self.system_instruction,
            generation_config={"temperature": 0.5}
        )

    def update_system_instruction(self, new_instruction):
        self.system_instruction = new_instruction
        self._initialize_model()

    def generate_suggestion_stream(self, current_transcript):
        prompt = f"Interviewer's Question / Statement:\n\n{current_transcript}"
        try:
            response = self.model.generate_content(prompt, stream=True)
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            yield f"[Error connecting to Gemini]\n{e}"
