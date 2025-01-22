import json
import tkinter as tk
from tkinter import filedialog, messagebox
from pinecone import Pinecone, ServerlessSpec

# Configure Pinecone API
PINECONE_API_KEY = ""  # Replace with your Pinecone API key
PINECONE_ENVIRONMENT = "us-east-1"  # Replace with your Pinecone environment (region)
INDEX_NAME = "ada"  # Replace with your Pinecone index name

# Initialize Pinecone client
pc = Pinecone(
    api_key=PINECONE_API_KEY
)

# Define the serverless specification
spec = ServerlessSpec(
    cloud="aws",
    region=PINECONE_ENVIRONMENT
)

# Check and connect to the index
if INDEX_NAME not in pc.list_indexes().names():
    raise ValueError(f"Index '{INDEX_NAME}' does not exist.")
index = pc.Index(INDEX_NAME)

# Function to read embeddings from JSON file
def load_embeddings_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Function to prepare data for Pinecone
def prepare_data_for_pinecone(embeddings):
    pinecone_data = []
    for item in embeddings:
        chunk_id = f"chunk-{item['chunk_id']}"  # Create a unique ID for each chunk
        vector = item['embedding']  # Embedding vector
        metadata = {"text": item["text"][:200]}  # Truncate metadata for efficiency
        pinecone_data.append((chunk_id, vector, metadata))
    return pinecone_data

# Function to upload embeddings to Pinecone
def upload_embeddings_to_pinecone(json_file_path):
    # Load embeddings from JSON
    embeddings = load_embeddings_from_json(json_file_path)

    # Validate dimensions of embeddings
    vector_dim = len(embeddings[0]['embedding'])
    if vector_dim != 1536:  # Ensure compatibility with the new index dimensions
        raise ValueError(f"Embedding dimensions {vector_dim} do not match index dimensions (1536).")

    # Prepare data for Pinecone
    pinecone_data = prepare_data_for_pinecone(embeddings)

    # Upsert data to Pinecone
    index.upsert(vectors=pinecone_data)
    print(f"Uploaded {len(pinecone_data)} items to Pinecone index '{INDEX_NAME}'.")
    messagebox.showinfo("Success", f"Uploaded {len(pinecone_data)} items to Pinecone index '{INDEX_NAME}'.")

# Create the main application window
def main():
    app = tk.Tk()
    app.title("Upload Embeddings to Pinecone")
    app.geometry("400x200")

    # Function to select and upload the JSON file
    def select_and_upload_file():
        json_file_path = filedialog.askopenfilename(
            title="Select JSON File",
            filetypes=[("JSON files", "*.json")]
        )

        if not json_file_path:
            messagebox.showwarning("No File Selected", "Please select a JSON file to upload.")
            return

        try:
            upload_embeddings_to_pinecone(json_file_path)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # UI Elements
    label = tk.Label(app, text="Select the JSON file containing embeddings:")
    label.pack(pady=10)

    upload_button = tk.Button(app, text="Select and Upload", command=select_and_upload_file)
    upload_button.pack(pady=20)

    app.mainloop()

if __name__ == "__main__":
    main()
