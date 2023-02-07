import tkinter as tk
from pytube import YouTube
from pytube import Playlist

count = 0


# function to name fix
def name_fix(name):
    # replace the invalid characters
    name = name.replace("/", "_")
    name = name.replace(":", "_")
    name = name.replace("?", "_")
    name = name.replace("*", "_")
    name = name.replace("<", "_")
    name = name.replace(">", "_")
    name = name.replace("|", "_")
    name = name.replace('"', "_")

    # return the new name
    return name

# function to rename the file
def new_name(name):
    # remove the file extension
    name = name.split(".")[0]

    # add the count to the file name
    name = str(count) + "_" + name

    # add the file extension
    name = name + ".mp3"

    # return the new name
    return name

class MainWindow:
    def __init__(self, master):
        self.master = master
        master.title("YouTube Audio Downloader")

        self.text_box = tk.Text(master, height=5, width=50)
        self.text_box.pack()

        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

        self.download_button = tk.Button(master, text="Download", command=self.updateResult)
        self.download_button.pack()

    def updateResult(self):
        text = self.text_box.get("1.0", "end-1c")
        self.text_box.config(state="disabled")
        yt_title = self.download_audio_playlist(text)
        self.result_label.config(text="Finished: " + yt_title)
        self.text_box.config(state="normal")

    def download_audio_playlist(self, playlist_url):
        global count

        yt_playlist = Playlist(playlist_url)

        # get the playlist title
        playlist_title = yt_playlist.title

        # get the list of video URLs
        video_urls = yt_playlist.video_urls

        # loop through the list of video URLs
        for url in video_urls:
            # create a YouTube object
            yt = YouTube(url)

            # get the audio stream
            audio = yt.streams.filter(only_audio=True).first()

            # Downloading report
            self.result_label.config(text="Downloading: " + yt.title)
            print("Downloading: " + yt.title)

            file = new_name(audio.default_filename)

            # download the audio file
            audio.download(name_fix(playlist_title), filename=file)

            self.result_label.config(text="Downloaded")
            print("Downloaded: " + new_name(audio.default_filename))

            # increment the count
            count += 1
        print("Finshed: " + playlist_title)

        return name_fix(playlist_title)

root = tk.Tk()
main_window = MainWindow(root)
root.mainloop()
