import customtkinter as ctk
import threading
import time

class StealthUI:
    def __init__(self, initial_prompt="", initial_timeout=3.0, on_settings_save_callback=None):
        ctk.set_appearance_mode("Dark")
        self.root = ctk.CTk()
        self.root.title("Stealth Interview Copilot")
        
        self.current_prompt = initial_prompt
        self.current_timeout = initial_timeout
        self.on_settings_save_callback = on_settings_save_callback

        # Make the window always on top and semi-transparent
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-alpha", 0.90)
        self.root.geometry("450x650+50+50")
        
        # Title Frame
        self.title_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.title_frame.pack(fill="x", pady=10, padx=10)
        
        self.title_label = ctk.CTkLabel(self.title_frame, text="Stealth Interview Copilot", font=("Helvetica", 16, "bold"), text_color="#4CAF50")
        self.title_label.pack(side="left", expand=True)

        self.settings_btn = ctk.CTkButton(self.title_frame, text="⚙️ Settings", width=60, fg_color="#4CAF50", hover_color="#45a049", command=self.open_settings)
        self.settings_btn.pack(side="right")
        
        # Scrollable Chat Area
        self.chat_frame = ctk.CTkScrollableFrame(self.root, fg_color="transparent")
        self.chat_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # To track live incoming speech
        self.current_question_bubble = None
        self.current_suggestion_bubble = None

    def open_settings(self):
        settings_win = ctk.CTkToplevel(self.root)
        settings_win.title("Copilot Settings")
        settings_win.geometry("500x440")
        settings_win.attributes("-topmost", True)
        
        lbl = ctk.CTkLabel(settings_win, text="System Prompt (Persona & Formatting)", font=("Helvetica", 14, "bold"))
        lbl.pack(pady=(10, 0))
        
        textbox = ctk.CTkTextbox(settings_win, width=460, height=220, font=("Helvetica", 13))
        textbox.pack(padx=20, pady=10)
        textbox.insert("1.0", self.current_prompt)
        
        timeout_lbl = ctk.CTkLabel(settings_win, text="AI Response Delay (Seconds to wait after speech stops):", font=("Helvetica", 12))
        timeout_lbl.pack(pady=(5,0))
        
        timeout_var = ctk.StringVar(value=str(self.current_timeout))
        timeout_entry = ctk.CTkEntry(settings_win, textvariable=timeout_var, width=60, justify="center")
        timeout_entry.pack(pady=(0,10))
        
        def save():
            new_prompt = textbox.get("1.0", "end-1c")
            try:
                new_timeout = float(timeout_var.get())
            except ValueError:
                new_timeout = self.current_timeout
                
            self.current_prompt = new_prompt
            self.current_timeout = new_timeout
            
            if self.on_settings_save_callback:
                self.on_settings_save_callback(new_prompt, new_timeout)
            settings_win.destroy()
            
        save_btn = ctk.CTkButton(settings_win, text="Save & Apply", command=save)
        save_btn.pack(pady=10)

    def _add_bubble(self, sender, text):
        bubble_frame = ctk.CTkFrame(self.chat_frame, corner_radius=15)
        
        if sender == "Interviewer":
            bubble_frame.configure(fg_color="#2B2D31") # Discord-like dark grey
            bubble_frame.pack(anchor="w", pady=5, padx=(0, 40), fill="x")
            text_color = "#E0E0E0"
            font_style = ("Helvetica", 14)
        else: # Copilot (AI)
            bubble_frame.configure(fg_color="#183D2A") # Dark Green
            bubble_frame.pack(anchor="e", pady=5, padx=(40, 0), fill="x")
            text_color = "#00FFA5"
            font_style = ("Helvetica", 14, "bold")

        # Create a text box or label that expands. Sub-label for sender name
        sender_lbl = ctk.CTkLabel(bubble_frame, text=sender, font=("Helvetica", 10, "italic"), text_color="#888888")
        sender_lbl.pack(anchor="w" if sender == "Interviewer" else "e", padx=10, pady=(5,0))

        lbl = ctk.CTkLabel(bubble_frame, text=text, text_color=text_color, justify="left", wraplength=320, font=font_style)
        lbl.pack(anchor="w" if sender == "Interviewer" else "e", padx=15, pady=(0, 10))
        
        # Scroll to bottom after adding
        self.root.after(50, self._scroll_to_bottom)
        
        return lbl

    def _scroll_to_bottom(self):
        try:
            self.chat_frame._parent_canvas.yview_moveto(1.0)
        except Exception:
            pass

    def update_question(self, text):
        def _update():
            if self.current_question_bubble is not None:
                self.current_question_bubble.configure(text=text)
            else:
                self.current_question_bubble = self._add_bubble("Interviewer", text)
            self._scroll_to_bottom()
        self.root.after(0, _update)

    def finish_question(self):
        def _update():
            self.current_question_bubble = None
        self.root.after(0, _update)

    def update_suggestion(self, text, is_loading=False):
        def _update():
            if self.current_suggestion_bubble is not None:
                self.current_suggestion_bubble.configure(text=text)
            else:
                self.current_suggestion_bubble = self._add_bubble("Copilot", text)
                
            if not is_loading:
                self.current_suggestion_bubble = None
                
            self._scroll_to_bottom()
        self.root.after(0, _update)

    def hide_window(self):
        self.root.after(0, self.root.withdraw)
        
    def show_window(self):
        self.root.after(0, self.root.deiconify)

    def start(self):
        self.root.mainloop()

if __name__ == "__main__":
    ui = StealthUI()
    def test_updates():
        time.sleep(1)
        q = "Can you explain the difference between SEO and SEM?"
        for i in range(1, len(q)+1):
            ui.update_question(q[:i])
            time.sleep(0.02)
            
        time.sleep(0.5)
        ans = "- SEO focuses on organic traffic\n- SEM includes paid advertising (PPC)\n- Both aim to increase visibility."
        ui.update_suggestion(ans)
        
        time.sleep(1)
        ui.update_question("That makes sense. What are some good SEO tools?")
        time.sleep(1)
        ui.update_suggestion("- Ahrefs\n- SEMrush\n- Google Search Console")
        
    threading.Thread(target=test_updates, daemon=True).start()
    ui.start()
