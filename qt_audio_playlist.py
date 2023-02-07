import sys
from pytube import YouTube
from pytube import Playlist
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QLabel

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



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.text_box = QTextEdit(self)
        self.text_box.move(20, 20)
        self.text_box.resize(280, 40)

        self.result_label = QLabel(self)
        self.result_label.move(20, 80)
        self.result_label.resize(280, 40)
        self.result_label.setText("")

        button = QPushButton("Download", self)
        button.move(20, 120)
        button.clicked.connect(self.updateResult)
        
        self.setGeometry(300, 300, 320, 200)
        self.setWindowTitle("youtube playlist audio downloader")
        self.show()
    
        # function to download the audio playlist
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
            self.result_label.setText("Downloading: " + yt.title)
            print("Downloading: " + yt.title)

            file = new_name(audio.default_filename)

            # download the audio file
            audio.download(name_fix(playlist_title), filename=file)

            self.result_label.setText("Downloaded")
            print("Downloaded: " + new_name(audio.default_filename))

            # increment the count
            count += 1
        print("Finshed: " + playlist_title)

        return name_fix(playlist_title)
    
    def updateResult(self):
        text = self.text_box.toPlainText()
        self.text_box.setEnabled(False)
        yt_tilte = self.download_audio_playlist(text)
        self.result_label.setText("Finshed: " + yt_tilte)
        self.text_box.setEnabled(True)

app = QApplication(sys.argv)
main_window = MainWindow()
sys.exit(app.exec_())
