"""
首次设置 PIN 码界面
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


class SetupPinScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._step = 'set'     # 'set' 或 'confirm'
        self._first_pin = ''
        self._input = ''
        self._focus_row = 0
        self._focus_col = 1
        self._btn_map = {}
        self._build_ui()

    def _build_ui(self):
        root = FloatLayout()
        with root.canvas.before:
            Color(*get_color_from_hex('#0D2137'))
            self._bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=self._update_bg, size=self._update_bg)

        wrapper = BoxLayout(
            orientation='vertical',
            spacing=30,
            size_hint=(0.45, 0.85),
            pos_hint={'center_x': 0.5, 'center_y': 0.52}
        )

        self.title_label = Label(
            text='欢迎使用护眼小卫士！\n请设置家长密码',
            font_size='40sp',
            color=get_color_from_hex('#FFD700'),
            halign='center',
            size_hint=(1, 0.2),
        )
        self.title_label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))

        self.dot_label = Label(
            text='○○○○',
            font_size='52sp',
            color=get_color_from_hex('#FFFFFF'),
            size_hint=(1, 0.1),
        )

        self.msg_label = Label(
            text='请输入4-6位数字密码',
            font_size='30sp',
            color=get_color_from_hex('#B2DFDB'),
            size_hint=(1, 0.1),
        )

        self.error_label = Label(
            text='',
            font_size='30sp',
            color=get_color_from_hex('#FF5252'),
            size_hint=(1, 0.08),
        )

        keypad_grid = GridLayout(cols=3, spacing=16, size_hint=(1, 0.52))
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

        wrapper.add_widget(self.title_label)
        wrapper.add_widget(self.dot_label)
        wrapper.add_widget(self.msg_label)
        wrapper.add_widget(self.error_label)
        wrapper.add_widget(keypad_grid)
        root.add_widget(wrapper)
        self.add_widget(root)

    def _update_bg(self, instance, value):
        self._bg.pos = instance.pos
        self._bg.size = instance.size

    def on_enter(self):
        self._step = 'set'
        self._first_pin = ''
        self._input = ''
        self.error_label.text = ''
        self._update_dots()
        self._set_focus(0, 1)

    def _update_dots(self):
        n = len(self._input)
        self.dot_label.text = '●' * n + '○' * max(0, 4 - n)

    def _on_key(self, key):
        if key == '←':
            self._input = self._input[:-1]
            self.error_label.text = ''
        elif key == '✓':
            self._confirm()
        elif len(self._input) < 6:
            self._input += key
        self._update_dots()

    def _confirm(self):
        if len(self._input) < 4:
            self.error_label.text = '密码至少需要4位'
            return
        if self._step == 'set':
            self._first_pin = self._input
            self._input = ''
            self._step = 'confirm'
            self.title_label.text = '请再次输入密码确认'
            self.msg_label.text = '再输入一次，确保记住了'
            self._update_dots()
        else:
            if self._input == self._first_pin:
                app = App.get_running_app()
                app.config_mgr.set_pin(self._input)
                app.sm.current = 'home'
                app.timer_service.start(app.config_mgr.reminder_interval)
            else:
                self.error_label.text = '两次输入不一致，请重新设置'
                self._step = 'set'
                self._first_pin = ''
                self._input = ''
                self.title_label.text = '欢迎使用护眼小卫士！\n请重新设置家长密码'
                self.msg_label.text = '请输入4-6位数字密码'
                self._update_dots()

    def _set_focus(self, row, col):
        old = self._btn_map.get((self._focus_row, self._focus_col))
        if old:
            old.background_color = get_color_from_hex('#1E3A5F')
        self._focus_row, self._focus_col = row, col
        new = self._btn_map.get((row, col))
        if new:
            new.background_color = get_color_from_hex('#4A9FD4')

    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        rows, cols = len(KEYPAD), 3
        r, c = self._focus_row, self._focus_col
        if key == 273:
            self._set_focus((r - 1) % rows, c); return True
        elif key == 274:
            self._set_focus((r + 1) % rows, c); return True
        elif key == 276:
            self._set_focus(r, (c - 1) % cols); return True
        elif key == 275:
            self._set_focus(r, (c + 1) % cols); return True
        elif key in (13, 32):
            btn = self._btn_map.get((r, c))
            if btn:
                self._on_key(btn.text)
            return True
        return False
