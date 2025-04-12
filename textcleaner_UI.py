import tkinter as tk
from tkinter import scrolledtext, messagebox
import spacy
import emoji

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Define unwanted POS tags (Penn Treebank format)
REMOVE_TAGS = {".",":"}

# Check if a token is an emoji
def is_emoji(token):
    return any(char in emoji.EMOJI_DATA for char in token.text)

# Clean text function
def clean_text():
    input_text = input_box.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showwarning("Warning", "Please enter some text!")
        return

    # Step 1: Remove emojis
    doc = nlp(input_text)
    tokens_without_emojis = [token for token in doc if not is_emoji(token)]
    cleaned_text1 = " ".join(token.text for token in tokens_without_emojis)

    # Step 2: Remove unwanted tags
    doc2 = nlp(cleaned_text1)
    cleaned_tokens = [token.text for token in doc2 if token.tag_ not in REMOVE_TAGS]
    cleaned_text2 = " ".join(cleaned_tokens)

    # Display cleaned text
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, cleaned_text2)

# Copy output to clipboard
def copy_to_clipboard():
    cleaned_text = output_box.get("1.0", tk.END).strip()
    if cleaned_text:
        root.clipboard_clear()
        root.clipboard_append(cleaned_text)
        messagebox.showinfo("Copied", "Cleaned text copied to clipboard!")

# --- UI Setup ---
root = tk.Tk()
root.title("Text Cleaner (POS + Emoji)")
root.geometry("600x600")

# Input label
tk.Label(root, text="Paste your text:").pack(pady=5)
input_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, font=("Arial", 12))
input_box.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# Clean button
tk.Button(root, text="Clean Text", command=clean_text, bg="#4CAF50", fg="white", padx=10).pack(pady=10)

# Output label
tk.Label(root, text="Cleaned Text:").pack(pady=5)
output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, font=("Arial", 12))
output_box.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# Copy button
tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard, bg="#2196F3", fg="white", padx=10).pack(pady=10)

# Run UI
root.mainloop()
