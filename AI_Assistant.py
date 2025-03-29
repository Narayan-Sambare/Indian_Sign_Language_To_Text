import tkinter as tk
from tkinter import scrolledtext
import google.generativeai as genai

# Configure the Generative AI Model
api_key = "AIzaSyDUZ5L1KMv6xMmUvQ3-ffr63xVCeNAHrPw"
genai.configure(api_key=api_key)

# Set up the model configuration and safety settings
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 512,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro-001",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Initialize a chat session
convo = model.start_chat(history=[])

class ChatbotApplication:
    def __init__(self, master):  # Corrected constructor name
        self.master = master
        master.title("Chatbot")
        master.geometry("500x600")
        master.resizable(False, False)
        master.configure(bg="#202020")

        # Text widget with a Scrollbar for chat history
        self.text_area = scrolledtext.ScrolledText(master, state='disabled', bg="#333333", fg="white", wrap=tk.WORD, font=("Arial", 10))
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Container for Entry and Send button
        entry_frame = tk.Frame(master, bg="#202020")
        entry_frame.pack(fill=tk.X, padx=10, pady=5)

        # Entry widget for messages
        self.entry_message = tk.Entry(entry_frame, bg="#404040", fg="white", font=("Arial", 12))
        self.entry_message.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
        self.entry_message.insert(0, "Type your message")
        self.entry_message.bind("<FocusIn>", self.on_entry_click)
        self.entry_message.bind("<FocusOut>", self.on_entry_focus_out)
        self.entry_message.bind("<Return>", self.send_message)

        # Send button
        self.send_button = tk.Button(entry_frame, text="Send", command=self.send_message, bg="#505050", fg="white", relief=tk.FLAT)
        self.send_button.pack(side=tk.RIGHT, ipadx=10, ipady=5, padx=(5, 0))

    def send_message(self, event=None):
        user_input = self.entry_message.get()
        if user_input and user_input != "Type your message":
            self.display_message("You: " + user_input)
            self.entry_message.delete(0, tk.END)  # Clear input field
            # Send input to the chatbot and get response
            response = self.get_chatbot_response(user_input)
            self.display_message("Chatbot: " + response)
    
    def display_message(self, message):
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, message + '\n')
        self.text_area.configure(state='disabled')
        self.text_area.see(tk.END)  # Scroll to the end

    def on_entry_click(self, event):
        """Clear the default text when the entry is clicked, if it is the default text."""
        if self.entry_message.get() == "Type your message":
            self.entry_message.delete(0, tk.END)

    def on_entry_focus_out(self, event):
        """Restore placeholder text if nothing is entered."""
        if not self.entry_message.get():
            self.entry_message.insert(0, "Type your message")

    def get_chatbot_response(self, user_input):
        # Send message to the chatbot model and receive a response
        convo.send_message(user_input)
        return convo.last.text

root = tk.Tk()
app = ChatbotApplication(root)
root.mainloop()