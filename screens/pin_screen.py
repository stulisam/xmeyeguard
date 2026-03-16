"""
PIN 码验证界面
遥控器操作：数字键盘用 DPAD 方向键导航，确认键选择
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.app import App
from kivy.utils import get_color_from_hex


KEYPAD = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['←', '0', '✓'],
]


class PinScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._input = ''
        self._next_screen = 'settings'
        self._on_verified_callback = None
        self._focus_row = 0
        self._focus_col = 0
        self._btn_map = {}
        self._build_ui()

    def set_next_screen(self, screen_name: str):
        self._next_screen = screen_name

    def set_on_verified(self, callback):
        self._on_verified_callback = callback

    def _build_ui(self):
        root = FloatLayout()
        with root.canvas.before:
            Color(*get_color_from_hex('#0D2137'))
            self._bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=self._update_bg, size=self._update_bg)

        wrapper = BoxLayout(
            orientation='vertical',
            spacing=30,
            size_hint=(0.45, 0.80),
            pos_hint={'center_x': 0.5, 'center_y': 0.52}
        )

        # 标题
        wrapper.add_widget(Label(
            text='请输入家长密码',
            font_size='44sp',
            color=get_color_from_hex('#FFD700'),
            size_hint=(1, 0.15),
        ))

        # 输入框显示（圆点）
        self.dot_label = Label(
            text='',
            font_size='52sp',
            color=get_color_from_hex('#FFFFFF'),
            size_hint=(1, 0.12),
        )
        wrapper.add_widget(self.dot_label)

        # 错误提示
        self.error_label = Label(
            text='',
            font_size='32sp',
            color=get_color_from_hex('#FF5252'),
            size_hint=(1, 0.1),
        )
        wrapper.add_widget(self.error_label)

        # 数字键盘
        keypad_grid = GridLayout(
            cols=3,
            spacing=16,
            size_hint=(1, 0.63),
        )
        for r, row in enumerate(KEYPAD):
            for c, key in enumerate(row):
                btn = Button(
                    text=key,
                    font_size='40sp',
                    background_normal='',
                    background_color=get_color_from_hex('#1E3A5F'),
                    color=get_color_from_hex('#FFFFFF'),
                )
                btn.bind(on_release=lambda inst, k=key: self._on_key(k))
                self._btn_map[(r, c)] = btn
                keypad_grid.add_widget(btn)

        wrapper.add_widget(keypad_grid)
        root.add_widget(wrapper)
        self.add_widget(root)

    def _update_bg(self, instance, value):
        self._bg.pos = instance.pos
        self._bg.size = instance.size

    def on_enter(self):
        self._input = ''
        self.error_label.text = ''
        self._update_dots()
        self._set_focus(0, 1)  # 默认聚焦到数字 5

    def _update_dots(self):
        self.dot_label.text = '●' * len(self._input) + '○' * max(0, 4 - len(self._input))

    def _on_key(self, key):
        if key == '←':
            self._input = self._input[:-1]
            self.error_label.text = ''
        elif key == '✓':
            self._verify()
        elif len(self._input) < 6:
            self._input += key
        self._update_dots()

    def _verify(self):
        app = App.get_running_app()
        if app.config_mgr.verify_pin(self._input):
            self.error_label.text = ''
            if self._on_verified_callback:
                cb = self._on_verified_callback
                self._on_verified_callback = None
                app.sm.current = self._next_screen
                cb()
            else:
                app.sm.current = self._next_screen
        else:
            self.error_label.text = '密码错误，请重试'
            self._input = ''
            self._update_dots()

    # ── 遥控器导航 ──────────────────────────────────────
    def _set_focus(self, row, col):
        # 取消旧焦点
        old_btn = self._btn_map.get((self._focus_row, self._focus_col))
        if old_btn:
            old_btn.background_color = get_color_from_hex('#1E3A5F')
        self._focus_row = row
        self._focus_col = col
        new_btn = self._btn_map.get((row, col))
        if new_btn:
            new_btn.background_color = get_color_from_hex('#4A9FD4')

    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        # 上273 下274 左276 右275 确认13
        rows = len(KEYPAD)
        cols = 3
        r, c = self._focus_row, self._focus_col
        if key == 273:    # UP
            self._set_focus((r - 1) % rows, c)
            return True
        elif key == 274:  # DOWN
            self._set_focus((r + 1) % rows, c)
            return True
        elif key == 276:  # LEFT
            self._set_focus(r, (c - 1) % cols)
            return True
        elif key == 275:  # RIGHT
            self._set_focus(r, (c + 1) % cols)
            return True
        elif key in (13, 32):  # 确认
            btn = self._btn_map.get((r, c))
            if btn:
                self._on_key(btn.text)
            return True
        return False
