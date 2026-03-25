# Stealth Interview Copilot 🕵️‍♂️🎤

Stealth Interview Copilot is an ultra-low latency, real-time AI assistant designed to listen to your interviews (or any audio stream) and provide instantaneous, live-streaming suggestions without taking up your entire screen.

It uses **SoundCard** (WASAPI) to intercept system audio without driver issues, **Deepgram** for lightning-fast speech-to-text, and **Google Gemini** for intelligent, context-aware responses.

![Demo](https://via.placeholder.com/800x400?text=Stealth+Interview+Copilot)

## Features 🚀
- **Zero-Latency Audio Capture:** Directly intercepts virtual audio cables using native Windows WASAPI loopback.
- **ChatGPT-Style Streaming:** AI answers are typed out in real-time as they are generated, completely eliminating perceived delays.
- **Smart Silence Detection:** Intelligently waits for the interviewer to finish their sentence before generating a response (Customizable Wait Time).
- **Dynamic Prompt Engineering:** Hot-swap your persona (e.g., "Software Engineer", "Marketing Expert") live from the in-app settings menu without restarting.
- **Stealth UI:** A dark-mode, semi-transparent, always-on-top window that sits unobtrusively on your screen.
- **Concurrency Locks:** Mutex locks prevent the AI from spawning multiple overlapping answers if the conversation gets chaotic.

---

## 🛠️ Installation & Setup

### 1. Requirements
- **Python 3.10+**
- **Windows OS** (Due to the `soundcard` library's WASAPI loopback optimizations)
- A Virtual Audio Cable. We highly recommend [VB-Audio Virtual Cable](https://vb-audio.com/Cable/) (Free).

### 2. Install Dependencies
Clone the repository, navigate to the folder, and install the required Python packages:
```bash
pip install -r requirements.txt
```

### 3. API Keys Configuration
This project requires two API keys to function:
1. **Deepgram API Key** (For Speech-to-Text) - [Get it here](https://console.deepgram.com/)
2. **Google Gemini API Key** (For AI Responses) - [Get it here](https://aistudio.google.com/)

Create a file named `.env` in the root directory (you can copy `.env.example`) and add your keys:
```env
DEEPGRAM_API_KEY=your_deepgram_api_key_here
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

### 4. Audio Routing (Crucial Step!) 🎧
To let the Copilot "hear" the interview (e.g., from Zoom or Google Meet), you must route your speakers into a Virtual Cable.
1. Install **VB-Audio Virtual Cable**.
2. Open Windows **Sound Settings** -> **More sound settings** -> **Recording** Tab.
3. Right-click **CABLE Output**, select **Properties**.
4. Go to the **Listen** tab. Check the box **"Listen to this device"**.
5. In the dropdown beneath it, select your **actual physical headphones/speakers**.
6. Click **Apply** and **OK**.
7. In Zoom/Meet, set your **Speaker/Output** to **CABLE Input**.

*Now, the audio flows from the meeting -> Virtual Cable (where the Copilot listens) -> Your Headphones.*

---

## 🏃‍♂️ Usage

Simply run the application from your terminal:
```bash
python main.py
```

- **F9 Key:** Press `F9` globally to instantly pause/hide the Copilot if you need to share your screen.
- **⚙️ Settings:** Click the gear icon to modify the AI's system prompt (Persona) or adjust the Silence Timeout delay mid-interview.

## Customizing the Persona
By default, the Copilot is a generic AI assistant. To make it perform perfectly for your specific interview, click the Settings button and enter something like:
> *"You are a Senior Frontend React Developer interviewing for a job. Answer technical questions confidently, use bullet points, and mention hooks or state management where applicable."*

Enjoy your interviews with confidence!
