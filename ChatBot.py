import random
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

# Define a function to handle user input
def chatbot_response(user_input):
    responses = {
        "hello": ["Hi there! How can I help you today?", "Hello! What can I do for you?", "Hey! How's it going?"],
        "how are you": ["I'm just a bot, but I'm doing great! How about you?", "I'm fine, thank you! How are you?", "Doing well! How can I assist you?"],
        "bye": ["Goodbye! Have a great day!", "See you later!", "Bye! Take care!"],
    }
    
    # Default response if the input is not recognized
    default_response = ["I'm sorry, I don't understand that.", "Can you please rephrase?", "I'm not sure what you mean."]

    # Return a random response if it exists, otherwise return a random default response
    return random.choice(responses.get(user_input.lower(), default_response))

# Function to handle sending messages
def send_message():
    user_input = user_entry.get()
    if user_input.strip() == "":
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chat_window.config(state='normal')
    chat_window.insert(tk.END, f"You ({timestamp}): {user_input}\n")
    response = chatbot_response(user_input)
    chat_window.insert(tk.END, f"ChatBot ({timestamp}): {response}\n")
    chat_window.config(state='disabled')
    chat_window.yview(tk.END)
    user_entry.delete(0, tk.END)
    if user_input.lower() == "bye":
        root.quit()

# Create the main window
root = tk.Tk()
root.title("ChatBot")

# Create a scrolled text widget for the chat window
chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, state='disabled', font=("Arial", 12))
chat_window.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Create an entry widget for user input
user_entry = tk.Entry(root, width=50, font=("Arial", 12))
user_entry.grid(row=1, column=0, padx=10, pady=10)

# Create a button to send the message
send_button = tk.Button(root, text="Send", command=send_message, font=("Arial", 12))
send_button.grid(row=1, column=1, padx=10, pady=10)

# Enable the chat window
chat_window.config(state='normal')
chat_window.insert(tk.END, "ChatBot: Hello! Type 'bye' to exit.\n")
chat_window.config(state='disabled')

# Run the main loop
root.mainloop()