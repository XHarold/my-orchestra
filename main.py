# main.py

import sys
from gestures import GestureRecognizer
from audio import AudioManager
from ui import OrchestraUI

def main():
    # 初始化模块
    print("Initializing modules...")
    recognizer = GestureRecognizer()
    audio_manager = AudioManager()
    ui = OrchestraUI()

    # 启动用户界面
    print("Launching UI...")
    ui_thread = ui.run()  # 假设 UI 模块以独立线程运行
    print("UI launched.")

    try:
        print("Starting gesture recognition...")
        while ui.is_running():
            # 获取手势数据
            gesture = recognizer.get_gesture()
            if gesture:
                print(f"Detected gesture: {gesture}")
                # 根据手势控制乐器演奏
                audio_manager.process_gesture(gesture)
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        # 关闭所有模块
        recognizer.close()
        audio_manager.close()
        ui.stop()

if __name__ == "__main__":
    main()
