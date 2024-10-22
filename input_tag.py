import time
import tkinter as tk
import pyautogui

# カンマ区切りの文字列
input_string = '''
horror, dark, suspense, mysterious, trap, atmospheric, cinematic, creepy, tense, urban, eerie, background_music, game_bgm, vlog_music, content_creator, royalty_free, instrumental, dark_trap, ambient, soundscape
'''
# 文字列をカンマで分割してリストに変換
input_list = [s.strip() for s in input_string.split(',')]

# カウントダウンウィンドウの設定
class CountdownWindow:
    def __init__(self, root):
        self.root = root
        self.label = tk.Label(root, text="入力開始タイマー", font=("Helvetica", 32))
        self.label.pack()
        self.countdown(5)

    def countdown(self, remaining=None):
        if remaining is not None:
            self.remaining = remaining
        if self.remaining <= 0:
            self.root.destroy()
        else:
            self.label.config(text=str(self.remaining))
            self.remaining -= 1
            self.root.after(1000, self.countdown)

# カウントダウンウィンドウの表示
root = tk.Tk()
root.geometry("300x100+0+0")  # ウィンドウのサイズと位置
root.overrideredirect(True)  # ウィンドウ枠を消す
root.attributes("-topmost", True)  # 常に最前面に表示
app = CountdownWindow(root)
root.mainloop()

# リスト形式の文字列を入力し、Enterキーを押す
for string in input_list:
    pyautogui.write(string)
    pyautogui.press('enter')
    time.sleep(0.5)  # 次の入力までの待機時間（必要に応じて調整）