from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget, QVideoWidgetControl
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QUrl, QTime
import json
class VideoPlayer(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("QTVideoPlayer")
        
        self.video = QVideoWidget()
        
        self.slider = QSlider(Qt.Horizontal)
        
        self.pauseButton = QPushButton()
        self.pauseButton.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_MediaPlay')))
        # self.pauseButton.setMaximumWidth(50)
        self.pauseButton.resize(50, 100)
        self.pauseButton.clicked.connect(self.changePlayState)
        
        self.volumeButton = QPushButton()
        self.volumeButton.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_MediaVolume')))
        
        self.currentTimeLabel = QLabel("00:00:00")
        self.totalTimeLabel = QLabel("00:00:00")
        
        self.controlsLayout = QHBoxLayout()  # Create a QHBoxLayout for the controls
        self.controlsLayout.addWidget(self.pauseButton)  # Add the play button to the controls layout
        self.controlsLayout.addWidget(self.volumeButton)
        self.controlsLayout.addStretch(1)
           
        self.timeLabelLayout = QHBoxLayout() # Create a QHBoxLayout for the time label
        self.timeLabelLayout.addWidget(self.currentTimeLabel)
        self.timeLabelLayout.addStretch(1) #Add stretchable space to the left of self.currentTimeLabel
        self.timeLabelLayout.addWidget(self.totalTimeLabel)
        self.timeLabelLayout.setAlignment(Qt.AlignBottom)
        
        self.layout = QVBoxLayout()  # QVBoxLayout to arrange these widgets in a column
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.video)
        self.layout.addLayout(self.timeLabelLayout)
        self.layout.addWidget(self.slider)
        self.layout.addLayout(self.controlsLayout)  # Add the controls layout to the main layout
        
        # Take up the space left after moving the timeLabel above slider
        # Comment it and see what happen, stretchFactor takes up extra space only
        self.layout.setStretchFactor(self.video, 1)
        self.layout.setStretchFactor(self.timeLabelLayout, 0)
        self.layout.setStretchFactor(self.slider, 0)
        self.layout.setStretchFactor(self.controlsLayout, 0)
    
        self.container = QWidget()  # Creating a QWidget to serve as a container for your QVideoWidget and QSlider
        self.container.setLayout(self.layout)  # Setting this layout on the QWidget with setLayout()
        
        self.setCentralWidget(self.container)  # Setting this QWidget as the central widget of your QMainWindow with setCentralWidget()
        
        menuBar = self.menuBar()
        media_menu = menuBar.addMenu("&File")
        media_menu.addAction("Open File")
        media_menu.addAction("Open Folder")
        media_menu.addSeparator()
        media_menu.addAction("Preference")
        media_menu.addSeparator()
        media_menu.addAction("Quit")
        
        audio_menu = menuBar.addMenu("&Audio")
        subtitle_menu = menuBar.addMenu("&Subtitle")
        
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.video)
        
        self.slider.sliderMoved.connect(self.player.setPosition)
        self.player.seekableChanged = True
        self.player.positionChanged.connect(self.update_position)
        self.player.durationChanged.connect(self.update_duration)
        
        self.video.showMaximized()
        
        
        self.showMaximized()
    
    def update_position(self, position):
        self.slider.setValue(position)
        self.currentTimeLabel.setText(QTime(0, 0).addMSecs(position).toString())
    
    def update_duration(self, duration):
        self.slider.setRange(0, duration)
        self.totalTimeLabel.setText(QTime(0, 0).addMSecs(duration).toString())
    
    def changePlayState(self):
        if self.player.state() == QMediaPlayer.StoppedState:
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile("./media/Test_Media.mp4")))
            self.player.play()
            self.pauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        elif self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.pauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        elif self.player.state() == QMediaPlayer.PausedState:
            self.player.play()
            self.pauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            
            
        
if __name__ == '__main__':
    app = QApplication([])
    player = VideoPlayer()
    app.exec_()
