import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re

# Function to tokenize text
def tokenize_text(text):
    return re.findall(r'\b\w+\b', text)

# Function to chunk text into smaller parts
def chunk_text(text, max_tokens=800):
    words = tokenize_text(text)
    chunks = []
    chunk = []
    count = 0
    for word in words:
        count += 1
        chunk.append(word)
        if count >= max_tokens:
            chunks.append(" ".join(chunk))
            chunk = []
            count = 0
    if chunk:
        chunks.append(" ".join(chunk))
    return chunks

# Function to handle file selection
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)

# Function to tokenize and chunk the selected file
def process_file():
    file_path = entry_file_path.get()
    if not file_path or not os.path.isfile(file_path):
        messagebox.showerror("Error", "Please select a valid .txt file")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Chunk the text
        chunks = chunk_text(text)

        # Save the chunked output
        output_file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            title="Save Chunked Output"
        )

        if output_file_path:
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write("\n\n".join(chunks))

            messagebox.showinfo("Success", f"Chunked output saved to {output_file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main application window
app = tk.Tk()
app.title("Text File Chunker")
app.geometry("400x200")

# UI elements
label_file_path = tk.Label(app, text="Select a .txt file:")
label_file_path.pack(pady=5)

entry_file_path = tk.Entry(app, width=50)
entry_file_path.pack(pady=5)

button_browse = tk.Button(app, text="Browse", command=select_file)
button_browse.pack(pady=5)

button_process = tk.Button(app, text="Chunk and Save", command=process_file)
button_process.pack(pady=20)

# Run the application
app.mainloop()
