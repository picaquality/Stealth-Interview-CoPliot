# VB-Audio Virtual Cable Setup Guide

To capture the interviewer's voice from Zoom without capturing your own voice (or to cleanly separate audio streams), we recommend using **VB-Audio Virtual Cable**.

## 1. Download & Install
1. Go to [VB-Audio Virtual Cable](https://vb-audio.com/Cable/) and download the appropriate version for Windows.
2. Extract the ZIP file.
3. Right-click on `VBCABLE_Setup_x64.exe` (or similar) and select **Run as Administrator**.
4. Click **Install Driver**, then reboot your computer when prompted.

## 2. Windows Sound Configuration
1. Open Windows **Settings** > **System** > **Sound**.
2. Under the "Related Settings" or Advanced, click on **More sound settings** (or the old Sound Control Panel).
3. Go to the **Recording** tab.
4. Find **CABLE Output**, right-click it, and select **Properties**.
5. Go to the **Listen** tab check the **Listen to this device** box.
6. Under "Playback through this device", select your actual physical headphones or speakers.
   - *Why do this?* This allows you to still hear the interviewer while the audio is routed through the virtual cable.
7. Click **Apply** and **OK**.

## 3. Zoom Setup
1. Open **Zoom** and go to **Settings** (gear icon) > **Audio**.
2. Set the **Speaker** dropdown to **CABLE Input (VB-Audio Virtual Cable)**.
3. Keep your **Microphone** set to your physical microphone (so the interviewer can still hear you).

## 4. Why this works
- When the interviewer speaks, their audio comes out of Zoom into "CABLE Input".
- Windows takes "CABLE Input" and routes it to "CABLE Output" (the recording side of the virtual cable).
- Since we enabled "Listen to this device", Windows duplicates the audio and sends it to your headphones so you can hear it.
- Our Python script (Interview Copilot) will simply listen to **CABLE Output** to capture ONLY the interviewer's voice with no cross-talk from your own microphone!
