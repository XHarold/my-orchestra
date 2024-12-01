import sys
import cv2
import mediapipe as mp
import pygame
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QPushButton, QDialog
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap

class CameraDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Camera Feed")
        self.setGeometry(100, 100, 640, 480)
        self.initUI()
        self.initCamera()
        self.initMediaPipe()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.video_label = QLabel()
        self.layout.addWidget(self.video_label)
        self.setLayout(self.layout)

    def initCamera(self):
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def initMediaPipe(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.mp_drawing = mp.solutions.drawing_utils

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(image))

    def closeEvent(self, event):
        self.cap.release()
        event.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gesture Controlled Audio Player")
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.button = QPushButton("Open Camera")
        self.button.clicked.connect(self.open_camera_dialog)
        self.layout.addWidget(self.button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def open_camera_dialog(self):
        self.camera_dialog = CameraDialog()
        self.camera_dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())