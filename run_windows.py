import tkinter as tk
from tkinter import ttk
import subprocess
import os

class CustomGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python GUI")
        self.root.geometry("800x480")
        self.root.configure(bg="#212121")  # Dark background color
        self.root.resizable(True, True)
        self.last_bracketed_mtime = None
        self.last_finalsub_mtime = None
        self.last_enter_mtime = None
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        self.create_widgets()
        self.watch_files()  # Start file watcher

    def watch_files(self):
        # Watch for changes in bracketed.json and finalsub.txt
        try:
            bracketed_mtime = os.path.getmtime("temp/bracketed.json")
            if self.last_bracketed_mtime != bracketed_mtime:
                self.last_bracketed_mtime = bracketed_mtime
                with open("temp/bracketed.json", "r", encoding="utf-8") as f:
                    output_content = f.read()
                self.left_textbox.delete("1.0", tk.END)
                self.left_textbox.insert(tk.END, output_content)
        except Exception as e:
            pass
        try:
            finalsub_mtime = os.path.getmtime("temp/finalsub.txt")
            if self.last_finalsub_mtime != finalsub_mtime:
                self.last_finalsub_mtime = finalsub_mtime
                with open("temp/finalsub.txt", "r", encoding="utf-8") as f:
                    output_content = f.read()
                self.right_textbox.delete("1.0", tk.END)
                self.right_textbox.insert(tk.END, output_content)
        except Exception as e:
            pass
        try:
            enter_mtime = os.path.getmtime("temp/enter.txt")
            if self.last_enter_mtime != enter_mtime:
                self.last_enter_mtime = enter_mtime
                with open("temp/enter.txt", "r", encoding="utf-8") as f:
                    output_content = f.read()
                self.evenrighter_textbox.delete("1.0", tk.END)
                self.evenrighter_textbox.insert(tk.END, output_content)
        except Exception as e:
            print(e)
            pass
        self.update_linecount()
        self.root.after(500, self.watch_files)

    def configure_styles(self):
        # Configure the main frame style
        self.style.configure("TFrame", background="#212121")

        # Configure button styles
        self.style.configure("TButton",
                             background="#424242",
                             foreground="white",
                             font=("Helvetica", 12),
                             bordercolor="white",
                             borderwidth=2,
                             relief="flat",
                             padding=10)
        self.style.map("TButton",
                       background=[("active", "#616161")])  # Lighter on hover

        # Configure entry and text styles
        self.style.configure("TEntry",
                             fieldbackground="#424242",
                             foreground="white",
                             font=("Helvetica", 12),
                             bordercolor="white",
                             borderwidth=2,
                             relief="flat")
        self.style.configure("TText",
                             background="#424242",
                             foreground="white",
                             font=("Helvetica", 12),
                             bordercolor="white",
                             borderwidth=2,
                             relief="flat")

        # Configure label style for the Topic
        self.style.configure("TLabel",
                             background="#212121",
                             foreground="white",
                             font=("Helvetica", 14, "bold"))

    def create_widgets(self):
        # Using a main frame with a grid layout
        main_frame = ttk.Frame(self.root, padding="15 15 15 15")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1, minsize=220)
        main_frame.columnconfigure(1, weight=1, minsize=220)
        main_frame.columnconfigure(2, weight=1, minsize=220)
        for i in range(5):  # Adjust rows as needed
            if i == 1:
                main_frame.rowconfigure(i, weight=1, minsize=120)  # Set minsize for textboxes
            else:
                main_frame.rowconfigure(i, weight=1)

        # Topic label and entry
        topic_frame = ttk.Frame(main_frame)
        topic_frame.grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky="ew")
        topic_frame.columnconfigure(0, weight=0)
        topic_frame.columnconfigure(1, weight=1)

        ttk.Label(topic_frame, text="Topic", style="TLabel").grid(row=0, column=0, padx=(0, 10), sticky="w")
        self.topic_entry = ttk.Entry(topic_frame, style="TEntry")
        self.topic_entry.insert(0, "Why do we all have that one friend who...")
        self.topic_entry.grid(row=0, column=1, sticky="ew")
        self.linecount_label = ttk.Label(topic_frame, text="5 5 5", style="TLabel")
        self.linecount_label.grid(row=0, column=2, padx=(10, 10))


        # Multiline Scrollable Textboxes (reversed order because me stupid)
        self.left_textbox = tk.Text(main_frame, wrap="word", relief="flat", bg="#424242", fg="white", font=("Helvetica", 12), bd=2, highlightthickness=2, highlightbackground="white", padx=5, pady=5, spacing3=8, width=30, height=8)
        self.left_textbox.grid(row=1, column=2, sticky="nsew", padx=(5, 0), pady=5)
        self.left_textbox.insert(tk.END, "Multiline Scrollable Textbox")

        self.right_textbox = tk.Text(main_frame, wrap="word", relief="flat", bg="#424242", fg="white", font=("Helvetica", 12), bd=2, highlightthickness=2, highlightbackground="white", padx=5, pady=5, spacing3=8, width=30, height=8)
        self.right_textbox.grid(row=1, column=1, sticky="nsew", padx=(5, 0), pady=5)
        self.right_textbox.insert(tk.END, "Multiline Scrollable Textbox")

        self.evenrighter_textbox = tk.Text(main_frame, wrap="word", relief="flat", bg="#424242", fg="white", font=("Helvetica", 12), bd=2, highlightthickness=2, highlightbackground="white", padx=5, pady=5, spacing3=8, width=30, height=8)
        self.evenrighter_textbox.grid(row=1, column=0, sticky="nsew", padx=(5, 0), pady=5)
        self.evenrighter_textbox.insert(tk.END, "Multiline Scrollable Textbox")

        # Regenerate buttons
        ttk.Button(main_frame, text="Generate All", command=self.on_regenerate_left).grid(row=2, column=0, sticky="ew", pady=2, padx=5)
        ttk.Button(main_frame, text="Regenerate Plain", command=self.on_regenerate_right).grid(row=2, column=1, sticky="ew", pady=2, padx=5)
        ttk.Button(main_frame, text="Regenerate Brackets", command=self.regen_br).grid(row=2, column=2, sticky="ew", pady=2, padx=5)

        ttk.Button(main_frame, text="Start TTS Server", command=self.on_prepare_file).grid(row=3, column=0, sticky="ew", pady=2, padx=5)
        ttk.Button(main_frame, text="Generate TTS", command=self.on_make_file).grid(row=3, column=1, sticky="ew", pady=2, padx=5)
        ttk.Button(main_frame, text="View File", command=self.on_view_file).grid(row=3, column=2, sticky="ew", pady=2, padx=5)

        # Start button at the bottom
        ttk.Button(main_frame, text="Make Video", command=self.on_start).grid(row=4, column=0, columnspan=1, sticky="ew", pady=2, padx=5)
        ttk.Button(main_frame, text="Clean Up",command=self.on_cleanup).grid(row=4, column=2, columnspan=1, sticky="ew", pady=2, padx=5)
        ttk.Button(main_frame, text="Open Result",command=self.on_openfinal).grid(row=4, column=1, columnspan=1, sticky="ew", pady=2, padx=5)

        self.left_textbox.bind("<<Modified>>", lambda e: self.on_text_modified(self.left_textbox, "temp/bracketed.json"))
        self.right_textbox.bind("<<Modified>>", lambda e: self.on_text_modified(self.right_textbox, "temp/finalsub.txt"))
        self.evenrighter_textbox.bind("<<Modified>>", lambda e: self.on_text_modified(self.evenrighter_textbox, "temp/enter.txt"))
        self.update_linecount()

    def update_linecount(self):
        left_lines = int(self.left_textbox.index('end-1c').split('.')[0]) # this code makes no sense
        right_lines = str(int(int(self.right_textbox.index('end-1c').split('.')[0]) + 1) / 2).replace('.0','') # What the fudge
        evenrighter_lines = int(self.evenrighter_textbox.index('end-1c').split('.')[0]) + 1 # compensate for the fact that the first textbox doesn't have "Subscribe." at the end
        self.linecount_label.config(text=f"{evenrighter_lines} {right_lines} {left_lines}")
        if int(left_lines) == int(right_lines) == int(evenrighter_lines): # wow weird chaining, cool
            self.linecount_label.config(text=f"Good")

    def on_text_modified(self, textbox, filename):
        if textbox.edit_modified():  # Only act if modified
            try:
                content = textbox.get("1.0", tk.END).rstrip("\n")
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(content)
                # update last_mtime so watch_files doesn’t immediately reload
                mtime = os.path.getmtime(filename)
                if filename == "temp/bracketed.json":
                    self.last_bracketed_mtime = mtime
                elif filename == "temp/finalsub.txt":
                    self.last_finalsub_mtime = mtime
                elif filename == "temp/enter.txt":
                    self.last_enter_mtime = mtime
            except Exception as e:
                print(f"Error writing to {filename}: {e}")
            finally:
                textbox.edit_modified(False)  # reset flag
                self.update_linecount()

    def run_generation(self):
        arg = self.topic_entry.get()
        print(f"Textbox content: {arg}")
        # Run makescript.bat in a new terminal window with the textbox content as an argument, ignore errors
        try:
            print(f'start cmd /k scripts\\batch\\makescript.bat "{arg}"')
            subprocess.run(f'start cmd /k scripts\\batch\\makescript.bat "{arg}"', shell=True)
        except Exception as e:
            print(f"(Ignored) Error running makescript.bat: {e}")
        print("Run finished")
        # After running, read output.txt and set left_textbox contents
        try:
            with open("temp/bracketed.json", "r", encoding="utf-8") as f:
                output_content = f.read()
            self.left_textbox.delete("1.0", tk.END)
            self.left_textbox.insert(tk.END, output_content)
        except Exception as e:
            print(f"Error reading enter.txt: {e}")
        try:
            with open("temp/finalsub.txt", "r", encoding="utf-8") as f:
                output_content = f.read()
            self.right_textbox.delete("1.0", tk.END)
            self.right_textbox.insert(tk.END, output_content)
        except Exception as e:
            print(f"Error reading finalsub.txt: {e}")

    def on_regenerate_left(self):
        print("Regenerate Left button pressed.")
        self.run_generation()

    def on_regenerate_right(self):
        print("Regenerate Right button pressed.")
        arg = self.topic_entry.get()
        try:
            subprocess.run(f'start cmd /k scripts\\batch\\limited_regenerate.bat "{arg}"', shell=True)
        except Exception as e:
            print(f"(Ignored) Error running limited_regenerate.bat: {e}")
        print(f"Right Textbox content: {self.right_textbox.get('1.0', tk.END).strip()}")

    def on_view_file(self):
        print("View File button pressed.")
        try:
            os.startfile("temp\\audio.wav")
        except Exception as e:
            print(f"(Ignored) Error opening audio.wav: {e}")

    def on_make_file(self):
        print("Make File button pressed.")
        try:
            subprocess.run(f'start cmd /C python scripts\\audio\\stupid.py', shell=True)
        except Exception as e:
            print(f"(Ignored) Error running makefile.py: {e}")

    def on_prepare_file(self):
        print("Prepare File button pressed.")
        try:
            subprocess.run(f'start cmd /K scripts\\batch\\condahelper.bat', shell=True)
        except Exception as e:
            print(f"(Ignored) Error running prepfile.py: {e}")

    def on_start(self):
        print("Start button pressed.")
        subprocess.run(f'start cmd /K scripts\\batch\\sad.bat', shell=True)
    def on_finish(self):
        print("Finish button pressed.")
        subprocess.run('start cmd /K scripts\\batch\\audio_effects.bat', shell=True)
    def regen_br(self):
        print("bregen pressed")
        subprocess.run('start cmd /K scripts\\batch\\regenbr.bat', shell=True)
    def on_cleanup(self):
        print("cleaning up")
        subprocess.run('start cmd /K "scripts\\batch\\clean up.bat"', shell=True)
    def on_openfinal(self):
        print("cleaning up")
        os.startfile("FINALVIDEO.mp4")

if __name__ == "__main__":
    root = tk.Tk()
    app = CustomGUI(root)
    root.mainloop()
