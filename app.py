# pip3 install faster-whisper
import tkinter as tk
from tkinter import filedialog
from faster_whisper import WhisperModel

class App:
    def __init__(self, master):
        self.master = master
        master.title("Whisper Transcriber")

        # Initialize Whisper
        model_size = "small"
        self.model = WhisperModel(model_size, device="auto", compute_type="int8")

        # Choose File button
        self.choose_file_button = tk.Button(master, text="Choose File", command=self.choose_file)
        self.choose_file_button.pack()

        # Label to display chosen file name
        self.chosen_file_label = tk.Label(master, text="")
        self.chosen_file_label.pack()

        # Tickbox for including timestamps
        self.include_timestamps_var = tk.BooleanVar()
        self.include_timestamps_tickbox = tk.Checkbutton(master, text="With Timestamp", variable=self.include_timestamps_var)
        self.include_timestamps_tickbox.pack()

        # Start button
        self.start_button = tk.Button(master, text="Start", command=self.start_transcription)
        self.start_button.pack()

        # Result text area
        self.result_text_area = tk.Text(master)
        self.result_text_area.pack(fill=tk.BOTH, expand=True)

    def choose_file(self):
        # Open file dialog and get chosen file path
        self.file_path = filedialog.askopenfilename()
        # Update chosen file label with file name
        self.chosen_file_label.config(text="Chosen file: " + self.file_path)

    def start_transcription(self):
        # Clear previous results from text area
        self.result_text_area.delete(1.0, tk.END)

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
        self.result_text_area.insert("1.0", f"TRANSCRIPTION WORD COUNT: {word_count}\n")

root = tk.Tk()
app = App(root)
root.mainloop()
