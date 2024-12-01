# ui.py

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGraphicsEllipseItem, QGraphicsScene, QGraphicsView
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor

class OrchestraUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 设置窗口属性
        self.setWindowTitle("Orchestra Gesture Control")
        self.showMaximized()

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)

        # 上部：半圆区域
        scene = QGraphicsScene()
        half_circle = QGraphicsEllipseItem(QRectF(-500, -250, 1000, 500))
        half_circle.setBrush(QColor("#87CEFA"))  # 使用淡蓝色填充
        half_circle.setPen(QColor("#4682B4"))   # 边框深蓝色
        scene.addItem(half_circle)

        view = QGraphicsView(scene)
        view.setAlignment(Qt.AlignCenter)
        view.setStyleSheet("background: transparent; border: none;")
        main_layout.addWidget(view, stretch=3)

        # 下部：摄像头画面和手势识别结果
        bottom_layout = QHBoxLayout()

        # 左侧摄像头画面
        self.camera_label = QLabel("Camera Feed")
        self.camera_label.setStyleSheet("background: black; color: white;")
        self.camera_label.setAlignment(Qt.AlignCenter)
        bottom_layout.addWidget(self.camera_label, stretch=2)

        # 右侧识别结果
        self.result_label = QLabel("Gesture Recognition Result")
        self.result_label.setStyleSheet("background: #D3D3D3; color: black;")
        self.result_label.setAlignment(Qt.AlignCenter)
        bottom_layout.addWidget(self.result_label, stretch=1)

        main_layout.addLayout(bottom_layout, stretch=1)

        # 设置主布局
        self.setLayout(main_layout)

    def update_camera_feed(self, image):
        """更新摄像头画面."""
        qt_image = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        self.camera_label.setPixmap(pixmap)

    def update_result(self, result):
        """更新手势识别结果."""
        self.result_label.setText(result)

    def run(self):
        """启动 UI."""
        self.show()

    def stop(self):
        """关闭 UI."""
        self.close()

    def is_running(self):
        """判断 UI 是否运行中."""
        return self.isVisible()

# 测试 UI
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = OrchestraUI()
    ui.run()
    sys.exit(app.exec_())
