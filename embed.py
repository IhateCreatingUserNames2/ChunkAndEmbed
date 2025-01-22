import openai
import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox

# Set your OpenAI API key
openai.api_key = ""

# Function to read chunks from a file
def read_chunks_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().split('\n\n')  # Assuming chunks are separated by double newlines

# Function to generate embeddings
def generate_embeddings(chunks):
    embeddings = []
    for i, chunk in enumerate(chunks):
        try:
            response = openai.Embedding.create(
                input=chunk,
                model="text-embedding-ada-002"
            )
            embedding = response["data"][0]["embedding"]
            embeddings.append({"chunk_id": i, "text": chunk, "embedding": embedding})
        except Exception as e:
            print(f"Error generating embedding for chunk {i}: {e}")
    return embeddings

# Function to save embeddings to a JSON file
def save_embeddings_to_file(embeddings, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(embeddings, file, indent=4)

# Function to handle file selection
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)

# Function to process file and generate embeddings
def process_file():
    file_path = entry_file_path.get()
    if not file_path or not os.path.isfile(file_path):
        messagebox.showerror("Error", "Please select a valid chunked .txt file.")
        return

    # Read chunks from the file
    chunks = read_chunks_from_file(file_path)

    # Generate embeddings
    print("Generating embeddings... This might take a while.")
    embeddings = generate_embeddings(chunks)

    # Save embeddings to a JSON file
    output_file_path = filedialog.asksaveasfilename(
        title="Save Embeddings JSON File",
        defaultextension=".json",
        filetypes=[("JSON files", "*.json")]
    )

    if output_file_path:
        save_embeddings_to_file(embeddings, output_file_path)
        messagebox.showinfo("Success", f"Embeddings saved to {output_file_path}")
    else:
        messagebox.showwarning("Canceled", "No file selected for saving embeddings.")

# Create the main application window
app = tk.Tk()
app.title("Text Embedding Generator")
app.geometry("400x200")

# UI elements
label_file_path = tk.Label(app, text="Select a chunked .txt file:")
label_file_path.pack(pady=5)

entry_file_path = tk.Entry(app, width=50)
entry_file_path.pack(pady=5)

button_browse = tk.Button(app, text="Browse", command=select_file)
button_browse.pack(pady=5)

button_process = tk.Button(app, text="Generate Embeddings", command=process_file)
button_process.pack(pady=20)

# Run the application
app.mainloop()
