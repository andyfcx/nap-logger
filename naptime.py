import os
import time
import datetime
from pynput import keyboard

log_directory = os.path.expanduser("~/Documents/worklog")
log_file = os.path.join(log_directory, "naptime.txt")
shortcut = {keyboard.Key.cmd, keyboard.Key.shift, keyboard.KeyCode(char='0')}
current_keys = set()
start_time = None

def on_press(key):
    global current_keys, start_time

    if key in shortcut:
        current_keys.add(key)
        if all(k in current_keys for k in shortcut):
            if start_time is None:
                # 開始計時
                start_time = datetime.datetime.now()
                print("午休計時開始...")
            else:
                # 停止計時並寫入時間
                end_time = datetime.datetime.now()
                nap_time = end_time - start_time
                nap_minutes = nap_time.seconds // 60
                print(f"午休時間：{nap_minutes} 分鐘")

                # 將午休時間寫入檔案
                with open(log_file, "a") as f:
                    f.write(f"{start_time} - {end_time} | 午休時間：{nap_time}分鐘")
                    f.write("========================\n")

                # 重置計時器
                start_time = None

def on_release(key):
    global current_keys

    if key in current_keys:
        current_keys.remove(key)

    if key == keyboard.Key.esc:
        return False

def create_log_directory():
    os.makedirs(log_directory, exist_ok=True)

def main():
    create_log_directory()
    print("按下 cmd+shift+0 開始午休計時...")
    
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()
