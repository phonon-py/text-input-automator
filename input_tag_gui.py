import flet as ft
import pyautogui
import time
from typing import List

class TextInputAutomation:
    def __init__(self):
        self.input_strings: List[str] = []
        self.is_counting = False
        
    def main(self, page: ft.Page):
        self.page = page
        # ウィンドウの設定
        page.title = "テキスト入力オートメーション"
        page.window.width = 600
        page.window.height = 400
        page.window.resizable = False
        
        # テキストフィールドの作成
        self.text_area = ft.TextField(
            multiline=True,
            min_lines=10,
            max_lines=15,
            width=550,
            label="カンマ区切りの文字列を入力してください",
            hint_text="例: text1, text2, text3",
        )
        
        # カウントダウン表示用のテキスト
        self.countdown_text = ft.Text(
            size=20,
            text_align=ft.TextAlign.CENTER,
            visible=False
        )
        
        # 実行ボタン
        self.execute_button = ft.ElevatedButton(
            text="実行",
            width=200,
            on_click=self.start_automation
        )
        
        # 画面レイアウト
        page.add(
            ft.Column(
                controls=[
                    self.text_area,
                    ft.Row(
                        controls=[self.execute_button],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    self.countdown_text
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            )
        )
    
    def parse_input(self) -> List[str]:
        """入力文字列をパースしてリストに変換"""
        text = self.text_area.value
        if not text:
            return []
        return [s.strip() for s in text.split(',') if s.strip()]
    
    def start_countdown(self):
        """カウントダウンの開始"""
        self.countdown_time = 5
        self.countdown_text.visible = True
        self.execute_button.disabled = True
        self.update_countdown()
        
    def update_countdown(self):
        """カウントダウンの更新"""
        if self.countdown_time >= 0:
            self.countdown_text.value = f"開始まで {self.countdown_time} 秒"
            self.countdown_time -= 1
            self.page.update()
            time.sleep(1)
            self.update_countdown()
        else:
            self.countdown_text.visible = False
            self.execute_button.disabled = False
            self.page.update()
            self.execute_automation()
    
    def execute_automation(self):
        """テキスト入力の自動化を実行"""
        for string in self.input_strings:
            pyautogui.write(string)
            pyautogui.press('enter')
            time.sleep(0.5)
    
    def start_automation(self, e):
        """自動化プロセスの開始"""
        self.input_strings = self.parse_input()
        if not self.input_strings:
            return
        
        # 別スレッドでカウントダウンを開始
        import threading
        countdown_thread = threading.Thread(target=self.start_countdown)
        countdown_thread.daemon = True
        countdown_thread.start()

if __name__ == "__main__":
    app = TextInputAutomation()
    ft.app(target=app.main)