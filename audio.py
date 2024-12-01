# audio.py

import pygame.midi

class AudioControllerMIDI:
    def __init__(self, midi_file):
        """初始化 MIDI 音频控制"""
        self.midi_file = midi_file
        pygame.midi.init()
        self.player = pygame.midi.Output(pygame.midi.get_default_output_id())
        self.volume = 100  # 默认音量（0-127）

    def play_midi(self):
        """播放 MIDI 文件"""
        from mido import MidiFile

        try:
            midi = MidiFile(self.midi_file)
            for msg in midi.play():
                if not msg.is_meta and msg.type in ('note_on', 'note_off'):
                    self.player.note_on(msg.note, self.volume if msg.type == 'note_on' else 0)
        except KeyboardInterrupt:
            self.stop_midi()

    def set_volume(self, volume):
        """
        设置音量（范围：0 - 1）。
        volume: 左手高度计算得出的音量值
        """
        self.volume = int(max(0, min(1, volume)) * 127)  # 转换到 MIDI 范围 0-127

    def stop_midi(self):
        """停止 MIDI 播放"""
        self.player.close()
        pygame.midi.quit()

# 测试代码
if __name__ == "__main__":
    from gestures import GestureRecognition
    import cv2

    # 初始化音频控制和手势识别
    audio_controller = AudioControllerMIDI("assets/example_music.mid")
    gesture_recognition = GestureRecognition()

    # 打开摄像头
    cap = cv2.VideoCapture(0)

    # 启动 MIDI 播放
    import threading
    threading.Thread(target=audio_controller.play_midi, daemon=True).start()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # 处理当前帧，获取手势结果
            annotated_frame, _ = gesture_recognition.process_frame(frame)

            # 示例逻辑：左手控制音量
            left_hand_height = 0.7  # 例如：从关键点位置得出的归一化值
            audio_controller.set_volume(left_hand_height)

            # 显示实时画面
            cv2.imshow("Gesture Recognition", annotated_frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        gesture_recognition.release()
        audio_controller.stop_midi()
