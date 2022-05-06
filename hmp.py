from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon
import sys
from yt_dlp import YoutubeDL

ydl = YoutubeDL()
 
class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Helios Media Player") 

        openButton = QPushButton("Open File")   
        openButton.setToolTip("Open Video File")
        openButton.setStatusTip("Open Video File")
        openButton.setFixedHeight(24)
        openButton.clicked.connect(self.openFile)
        
        openURLButton = QPushButton("Open URL")
        openURLButton.setToolTop("Open URL")
        openURLButton.setStatusTip("Open URL")
        openURLButton.setFixedHeight(24)
        openURLButton.clicked.connect(self.openURL)
 
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
 
        videoWidget = QVideoWidget()
 
        self.playButton = QPushButton("Play")
        self.playButton.setEnabled(False)
        self.playButton.clicked.connect(self.play)

        self.stopButton = QPushButton("Stop")
        self.stopButton.setEnabled(False)
        self.stopButton.clicked.connect(self.stop)
 
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.mediaTimer = QLabel("0s")
        self.slashLabel = QLabel("/")
        self.mediaTotal = QLabel("0s")
 
        self.error = QLabel()
        self.error.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum) 
 
        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)
 
        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.stopButton)
        controlLayout.addWidget(self.positionSlider)
        controlLayout.addWidget(self.mediaTimer)
        controlLayout.addWidget(self.slashLabel)
        controlLayout.addWidget(self.mediaTotal)
 
        layout = QVBoxLayout()
        layout.addWidget(openButton)
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.error)
 
        # Set widget to contain window contents
        wid.setLayout(layout)
 
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

        finish = QAction("Quit", self)
        finish.triggered.connect(self.exitCall)
 
    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath())
 
        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
            self.stopButton.setEnabled(True)
        
    def openURL(self):
        fileURL, _ = QtWidgets.QInputDialog.getText(self, "Open URL", "Enter the URL: ")
        
        if fileURL != '':
                if "youtube.com" in fileURL or "youtu.be" in fileURL:
                        try:
                                ytURL = ydl.extract_info(ytlink, download=False)
                                self.mediaPlayer.setMedia(QUrl(ytURL))
                        except:
                                handleError()
                else:
                        try:
                                self.mediaPlayer.setMedia(QUrl(fileURL))
                        except:
                                handleError()
                                
                self.playButton.setEnabled(True)
                self.stopButton.setEnabled(True)
 
    def exitCall(self):
        self.mediaPlayer.stop()
        quit()
        sys.exit()
 
    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def stop(self):
        self.mediaPlayer.stop()
 
    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setText("Pause")
        else:
            self.playButton.setText("Play")
 
    def positionChanged(self, position):
        self.positionSlider.setValue(position)
        self.mediaTimer.setText(str(int(position/1000)) + "s")
 
    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
        self.mediaTotal.setText(str(int(duration/1000)) + "s")
 
    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
 
    def handleError(self):
        self.playButton.setEnabled(False)
        self.error.setText("Error: " + self.mediaPlayer.errorString())
 
 
app = QApplication(sys.argv)
videoplayer = VideoPlayer()
videoplayer.resize(640, 480)
videoplayer.show()
sys.exit(app.exec_())
