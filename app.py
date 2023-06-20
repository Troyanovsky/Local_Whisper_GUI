# pip3 install faster-whisper
import argparse
import tkinter as tk
from tkinter import filedialog
from faster_whisper import WhisperModel
import os

# Add this function to parse command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Whisper Transcriber")
    parser.add_argument(
        "-m",
        "--model-size",
        default="small",
        choices=["tiny","base","small","meidum","large-v1","large-v2"],
        help="Choose the Whisper model size (tiny, base, small, medium, large-v1, large-v2). Add '.en' after model size for English-only models. Default is small.",
    )
    parser.add_argument(
        "-d",
        "--device",
        default="auto",
        choices=["auto", "cpu", "cuda"],
        help="Choose the device to run the transcription on (auto or cpu or cuda). Default is auto.",
    )
    return parser.parse_args()

class App:
    def __init__(self, master, model_size, device):
        self.master = master
        master.title("Whisper Transcriber")
        
        # Set initial window size
        master.geometry("1280x720")

        # Initialize Whisper
        self.model = WhisperModel(model_size, device=device, compute_type="int8")

        # Choose File button
        self.choose_file_button = tk.Button(master, text="Choose File", command=self.choose_file)
        self.choose_file_button.grid(row=0, column=0, padx=10, pady=10)

        # Label to display chosen file name
        self.chosen_file_label = tk.Label(master, text="")
        self.chosen_file_label.grid(row=0, column=1, padx=10, pady=10)

        # Start button
        self.start_button = tk.Button(master, text="Start", command=self.start_transcription)
        self.start_button.grid(row=1, column=0, padx=10, pady=10)

        # Tickbox for including timestamps
        self.include_timestamps_var = tk.BooleanVar()
        self.include_timestamps_tickbox = tk.Checkbutton(master, text="With Timestamp", variable=self.include_timestamps_var)
        self.include_timestamps_tickbox.grid(row=1, column=1, padx=10, pady=10)

        # Detected language label
        self.detected_language_label = tk.Label(master, text="Detected language: None")
        self.detected_language_label.grid(row=2, column=0, padx=10, pady=10)

        # Word count label
        self.word_count_label = tk.Label(master, text="Transcription word count: None")
        self.word_count_label.grid(row=2, column=1, padx=10, pady=10)

        # Result text area
        self.result_text_area = tk.Text(master)
        self.result_text_area.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Configure row and column resizing
        master.grid_rowconfigure(3, weight=1)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)

    def choose_file(self):
        # Open file dialog and get chosen file path
        self.file_path = filedialog.askopenfilename()
        # Get the file name from the file path
        file_name = os.path.basename(self.file_path)
        # Update chosen file label with file name
        self.chosen_file_label.config(text="Chosen file: " + file_name)

    def start_transcription(self):
        # Clear previous results from text area
        self.result_text_area.delete(1.0, tk.END)
        info = ""
        try:
            # Perform transcription
            segments, info = self.model.transcribe(self.file_path, beam_size=5, vad_filter=True)
            if segments:
                result_text = ""
                for segment in segments:
                    if self.include_timestamps_var.get():
                        result_text = result_text + "[%.2fs -> %.2fs] %s\n" % (segment.start, segment.end, segment.text)
                    else:
                        result_text = result_text + segment.text + "\n"
                self.result_text_area.delete(1.0, tk.END)
                self.result_text_area.insert(tk.END, result_text)
                # Display final result in text area
                if not result_text.strip():
                    self.result_text_area.insert(tk.END, "No speech detected in selected file.")
            else:
                self.result_text_area.insert(tk.END, "No speech detected in selected file.")
        except Exception as e:
            self.result_text_area.insert(tk.END, "Error: " + str(e))

        # Count the number of words in the transcription
        word_count = len(self.result_text_area.get("1.0", "end-1c").split())
        # Display word count at the top of the transcription
        self.word_count_label.config(text=f"Transcription word count: {word_count}\n")
        if info:
            self.detected_language_label.config(text="Detected language '%s' with probability %f" % (info.language, info.language_probability))

# Modify the following lines to pass the model_size to the App class
if __name__ == "__main__":
    args = parse_args()
    root = tk.Tk()
    app = App(root, args.model_size, args.device)
    root.mainloop()
