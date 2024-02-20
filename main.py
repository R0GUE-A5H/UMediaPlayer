from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget, QVideoWidgetControl
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QUrl, QTimer

class VideoPlayer(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("QTVideoPlayer")
        
        self.video = QVideoWidget()
        
        self.slider = QSlider(Qt.Horizontal)
        self.pauseButton = QPushButton()
        self.pauseButton.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_MediaPlay')))
        self.pauseButton.setMaximumWidth(50)
        
        
        
        #self.pauseButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        self.controlsLayout = QHBoxLayout()  # Create a QHBoxLayout for the controls
        self.controlsLayout.addWidget(self.pauseButton)  # Add the play button to the controls layout
        
        self.layout = QVBoxLayout()  # QVBoxLayout to arrange these widgets in a column
        self.layout.addWidget(self.video)
        self.layout.addWidget(self.slider)
        self.layout.addLayout(self.controlsLayout)  # Add the controls layout to the main layout
        
        self.container = QWidget()  # Creating a QWidget to serve as a container for your QVideoWidget and QSlider
        self.container.setLayout(self.layout)  # Setting this layout on the QWidget with setLayout()
        
        self.setCentralWidget(self.container)  # Setting this QWidget as the central widget of your QMainWindow with setCentralWidget()
        
        
        #TODO: --NOT WORKING---
        self.container.setContentsMargins(0, 0, 0, 0)
        
        menuBar = self.menuBar()
        media_menu = menuBar.addMenu("&File")
        media_menu.addAction("Open File")
        media_menu.addAction("Open Folder")
        media_menu.addSeparator()
        media_menu.addAction("Quit")
        
        audio_menu = menuBar.addMenu("&Audio")
        subtitle_menu = menuBar.addMenu("&Subtitle")
        
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.video)
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile("./test.mp4")))
        
        self.slider.sliderMoved.connect(self.player.setPosition)
        self.player.seekableChanged = True
        self.player.positionChanged.connect(self.slider.setValue)
        self.player.durationChanged.connect(self.update_position)
        
        self.video.showMaximized()
        self.player.play()
        
        self.showMaximized()
    
    def update_position(self, duration):
        self.slider.setRange(0, duration)
        
if __name__ == '__main__':
    app = QApplication([])
    player = VideoPlayer()
    app.exec_()
