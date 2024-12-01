# gestures.py

import cv2
import mediapipe as mp
import numpy as np

class GestureRecognition:
    def __init__(self):
        # 初始化 MediaPipe 手部模块
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils

    def process_frame(self, frame):
        """
        处理一帧图像，返回带注释的图像和手势识别结果。
        """
        frame = cv2.flip(frame, 1)  # 水平翻转图像
        # 转换颜色空间为 RGB（MediaPipe 需要）
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 使用 MediaPipe 处理图像
        result = self.hands.process(rgb_frame)

        # 初始化绘图结果
        annotated_frame = frame.copy()
        gesture_result = "No hands detected"

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # 绘制手部关键点和连接线
                self.mp_drawing.draw_landmarks(annotated_frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                # 提取手势信息（此处示例为检测举起手指的数量）
                finger_status = self.detect_finger_status(hand_landmarks)
                gesture_result = f"Fingers Up: {finger_status.count(1)}"

        return annotated_frame, gesture_result

    def detect_finger_status(self, hand_landmarks):
        """
        检测手指的状态(竖起为 1,弯曲为 0).
        """
        finger_tips = [4, 8, 12, 16, 20]
        finger_pips = [3, 6, 10, 14, 18]
        finger_status = []

        for tip, pip in zip(finger_tips, finger_pips):
            tip_pos = hand_landmarks.landmark[tip]
            pip_pos = hand_landmarks.landmark[pip]
            # 判断手指尖是否高于关节（简单判断手指是否竖起）
            if tip_pos.y < pip_pos.y:
                finger_status.append(1)  # 手指竖起
            else:
                finger_status.append(0)  # 手指弯曲

        return finger_status

    def release(self):
        """释放资源"""
        self.hands.close()

# 测试代码
if __name__ == "__main__":
    from ui import OrchestraUI
    import sys
    from PyQt5.QtWidgets import QApplication

    # 初始化应用
    app = QApplication(sys.argv)
    ui = OrchestraUI()
    gesture_recognition = GestureRecognition()

    # 打开摄像头
    cap = cv2.VideoCapture(0)

    def update_ui():
        """更新 UI 的回调函数"""
        ret, frame = cap.read()
        if not ret:
            return

        # 处理当前帧
        annotated_frame, gesture_result = gesture_recognition.process_frame(frame)

        # 更新到 UI
        ui.update_camera_feed(cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB))
        ui.update_result(gesture_result)

    # 启动 UI 并循环更新摄像头画面
    ui.show()

    # 用计时器持续更新画面
    from PyQt5.QtCore import QTimer
    timer = QTimer()
    timer.timeout.connect(update_ui)
    timer.start(30)

    # 关闭应用时释放资源
    exit_code = app.exec_()
    cap.release()
    gesture_recognition.release()
    sys.exit(exit_code)
