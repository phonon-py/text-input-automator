import flet as ft
import pyautogui
import time
from typing import List, Dict
from datetime import datetime
import json

class EnhancedTextAutomation:
    def __init__(self):
        self.input_strings: List[str] = []
        self.templates: Dict[str, List[str]] = {}
        self.current_template: str = ""
        self.is_counting = False
        
    def main(self, page: ft.Page):
        self.page = page
        page.title = "拡張テキスト入力オートメーション"
        page.window.width = 800
        page.window.height = 600
        page.window.resizable = False
        
        # テンプレート選択用ドロップダウン
        self.template_dropdown = ft.Dropdown(
            width=550,
            label="テンプレート選択",
            options=[
                ft.dropdown.Option("business_email", "ビジネスメール定型文"),
                ft.dropdown.Option("daily_report", "日報テンプレート"),
                ft.dropdown.Option("custom", "カスタム入力"),
            ],
            on_change=self.template_changed
        )
        
        # テキストフィールド
        self.text_area = ft.TextField(
            multiline=True,
            min_lines=10,
            max_lines=15,
            width=550,
            label="テキスト入力",
            hint_text="テンプレートを選択するか、カスタムテキストを入力"
        )
        
        # 遅延設定用スライダー
        self.delay_slider = ft.Slider(
            min=0.1,
            max=2.0,
            value=0.5,
            label="入力遅延(秒)",
            width=550
        )
        
        # ホットキー設定
        self.hotkey_field = ft.TextField(
            width=550,
            label="中断用ホットキー",
            value="esc",
            read_only=True
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
        
        # テンプレート保存ボタン
        self.save_template_button = ft.ElevatedButton(
            text="現在の入力をテンプレートとして保存",
            width=250,
            on_click=self.save_current_template
        )
        
        # 画面レイアウト
        page.add(
            ft.Column(
                controls=[
                    self.template_dropdown,
                    self.text_area,
                    self.delay_slider,
                    self.hotkey_field,
                    ft.Row(
                        controls=[self.execute_button, self.save_template_button],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    self.countdown_text
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            )
        )
        
        # テンプレートの読み込み
        self.load_templates()
    
    def template_changed(self, e):
        """テンプレート選択時の処理"""
        template_key = self.template_dropdown.value
        if template_key in self.templates:
            self.text_area.value = "\n".join(self.templates[template_key])
            self.page.update()
    
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
    
    def save_current_template(self, e):
        """現在の入力をテンプレートとして保存"""
        template_name = f"custom_template_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.templates[template_name] = self.parse_input()
        self.save_templates()
        
        # ドロップダウンの選択肢を更新
        self.template_dropdown.options.append(
            ft.dropdown.Option(template_name, f"カスタムテンプレート {len(self.templates)}")
        )
        self.page.update()
    
    def load_templates(self):
        """保存済みテンプレートの読み込み"""
        try:
            with open('templates.json', 'r', encoding='utf-8') as f:
                self.templates = json.load(f)
        except FileNotFoundError:
            self.templates = {
                "business_email": [
                    "お世話になっております。",
                    "ご連絡ありがとうございます。",
                    "以上、よろしくお願いいたします。"
                ],
                "daily_report": [
                    "【本日の業務内容】",
                    "1.",
                    "【明日の予定】",
                    "1.",
                    "【課題・懸念事項】"
                ]
            }
    
    def save_templates(self):
        """テンプレートの保存"""
        with open('templates.json', 'w', encoding='utf-8') as f:
            json.dump(self.templates, f, ensure_ascii=False, indent=2)

    def execute_automation(self):
        """拡張された自動入力実行"""
        delay = self.delay_slider.value
        
        for string in self.input_strings:
            # ESCキーでの中断チェック
            if pyautogui.position().x == 0 and pyautogui.position().y == 0:
                break
                
            lines = string.split('\n')
            for line in lines:
                pyautogui.write(line)
                pyautogui.press('enter')
                time.sleep(delay)
            
            # 段落間の追加ディレイ
            time.sleep(delay * 2)

if __name__ == "__main__":
    app = EnhancedTextAutomation()
    ft.app(target=app.main)