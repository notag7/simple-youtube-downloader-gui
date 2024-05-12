import os
from pytube import YouTube, exceptions
from time import time
from tkinter import *
from tkinter import filedialog
from customtkinter import *

# Initialize all the settings
set_appearance_mode("System")
set_default_color_theme("blue")




def download_video(video_url, download_location):
    try:
        start_time = time()
        yt = YouTube(video_url)
        stream = yt.streams.get_highest_resolution()  # Choose the highest resolution stream
        file_path = os.path.join(download_location, yt.title + '.mp4')
        stream.download(output_path=download_location, filename=file_path)
        end_time = time()

        popup = CTk()
        popup.title("Download Status")
        popup.resizable(True, True)
        popup.geometry("200x100")
        popup.grid_columnconfigure(0, weight=1)
        popup.grid_rowconfigure((0, 1), weight=1)
        msg = StringVar()
        msg.set(f"Download successful!\nTotal time taken: {round(end_time - start_time, 3)} seconds")
        label = CTkLabel(popup, text=msg.get())
        label.grid(row=0, column=0)
        button = CTkButton(popup, text="OK", command=popup.destroy)
        button.grid(row=1, column=0)
        popup.mainloop()
    except exceptions.AgeRestrictedError as age_error:
        error = CTk()
        error.title("Error")
        error.resizable(False, False)
        error.geometry("300x100")
        error.grid_rowconfigure((0, 1), weight=1)
        error.grid_columnconfigure(0, weight=1)
        error_label = CTkLabel(error, text=f"This video is age restricted:\n{age_error}")
        error_label.grid(row=0, column=0)
        button = CTkButton(error, text="OK", command=error.destroy)
        button.grid(row=1, column=0)
        error.mainloop()
    except exceptions.RegexMatchError:
        error = CTk()
        error.title("Error")
        error.resizable(False, False)
        error.geometry("300x100")
        error.grid_rowconfigure((0, 1), weight=1)
        error.grid_columnconfigure(0, weight=1)
        error_label = CTkLabel(error, text="Please enter a valid YouTube link")
        error_label.grid(row=0, column=0)
        button = CTkButton(error, text="OK", command=error.destroy)
        button.grid(row=1, column=0)
        error.mainloop()

def select_folder():
    download_location = filedialog.askdirectory()
    if download_location:
        entry_output.delete(0, END)
        entry_output.insert(0, download_location)

# Initializing the layout of the app
master = CTk()
master.title("YouTube Downloader")
master.grid_rowconfigure((0, 1), weight=1)
master.grid_columnconfigure((0, 1), weight=1)
master.geometry("400x150")
master.resizable(False, False)
CTkLabel(master, text="YouTube video URL:").grid(row=0, column=0)
entry_url = CTkEntry(master)
entry_url.grid(row=0, column=1)
CTkLabel(master, text="Output Folder:").grid(row=1, column=0)
entry_output = CTkEntry(master)
entry_output.grid(row=1, column=1)
CTkButton(master, text='Select Folder', command=select_folder).grid(row=1, column=2)
CTkButton(master, text='Download', command=lambda: download_video(entry_url.get(), entry_output.get())).grid(row=2, column=0, columnspan=3)
master.mainloop()
