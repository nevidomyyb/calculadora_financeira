from decimal import Decimal, ROUND_HALF_UP

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock

Window.size = (420, 780)

KV = '''
<InputRow>:
    size_hint_y: None
    height: dp(50)
    spacing: dp(8)
    padding: [dp(6), dp(4), dp(6), dp(4)]

    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(8)]

    Label:
        text: root.index_label
        font_size: dp(12)
        color: 0.55, 0.55, 0.65, 1
        size_hint_x: None
        width: dp(28)
        halign: 'center'
        valign: 'middle'
        text_size: self.width, self.height

    TextInput:
        id: txt
        hint_text: 'Ex: 1500.00'
        multiline: False
        font_size: dp(15)
        padding: [dp(10), dp(10)]
        background_color: 0, 0, 0, 0
        foreground_color: 0.1, 0.1, 0.15, 1
        cursor_color: 0.18, 0.42, 0.78, 1
        hint_text_color: 0.70, 0.70, 0.75, 1
        on_text: root.on_value_changed(self.text)

    Button:
        text: 'x'
        size_hint_x: None
        width: dp(36)
        background_normal: ''
        background_color: 0, 0, 0, 0
        color: 0.75, 0.22, 0.22, 1
        font_size: dp(17)
        bold: True
        on_press: root.do_remove()


<ResultCard>:
    size_hint_y: None
    height: dp(56)
    padding: [dp(16), dp(6)]

    canvas.before:
        Color:
            rgba: root.bg_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(10)]

    Label:
        text: root.card_title
        font_size: dp(13)
        color: root.lbl_color
        halign: 'left'
        valign: 'middle'
        text_size: self.width, self.height
        size_hint_x: 0.58

    Label:
        text: root.card_value
        font_size: dp(15)
        bold: True
        color: root.val_color
        halign: 'right'
        valign: 'middle'
        text_size: self.width, self.height
        size_hint_x: 0.42


<MainScreen>:
    orientation: 'vertical'
    padding: [dp(16), dp(20), dp(16), dp(16)]
    spacing: dp(10)

    canvas.before:
        Color:
            rgba: 0.93, 0.94, 0.97, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # ── Header ────────────────────────────────────────────────
    BoxLayout:
        size_hint_y: None
        height: dp(64)
        padding: [dp(16), dp(10)]
        spacing: dp(8)

        canvas.before:
            Color:
                rgba: 0.15, 0.37, 0.72, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(14)]

        Label:
            text: 'Calculadora Financeira'
            font_size: dp(18)
            bold: True
            color: 1, 1, 1, 1
            halign: 'left'
            valign: 'middle'
            text_size: self.width, self.height

        Label:
            id: counter_lbl
            text: '1/10'
            font_size: dp(11)
            color: 0.75, 0.88, 1, 0.9
            halign: 'right'
            valign: 'middle'
            text_size: self.width, self.height
            size_hint_x: None
            width: dp(42)

    # ── Input label ───────────────────────────────────────────
    Label:
        text: 'Valores de Entrada'
        font_size: dp(13)
        bold: True
        color: 0.28, 0.30, 0.42, 1
        size_hint_y: None
        height: dp(22)
        halign: 'left'
        text_size: self.width, self.height
        valign: 'bottom'

    # ── Inputs scroll ─────────────────────────────────────────
    ScrollView:
        size_hint_y: None
        height: min(inputs_grid.minimum_height, dp(200))
        do_scroll_x: False
        bar_width: dp(3)
        bar_color: 0.5, 0.6, 0.8, 0.6

        GridLayout:
            id: inputs_grid
            cols: 1
            spacing: dp(6)
            size_hint_y: None
            height: self.minimum_height

    # ── Add button ────────────────────────────────────────────
    Button:
        id: add_btn
        text: '+  Adicionar Valor'
        size_hint_y: None
        height: dp(42)
        background_normal: ''
        background_color: 0.12, 0.56, 0.40, 1
        color: 1, 1, 1, 1
        font_size: dp(14)
        bold: True
        on_press: root.add_input()

    # ── Divider ───────────────────────────────────────────────
    BoxLayout:
        size_hint_y: None
        height: dp(1)
        canvas.before:
            Color:
                rgba: 0.76, 0.80, 0.88, 1
            Rectangle:
                pos: self.pos
                size: self.size

    # ── Results label ─────────────────────────────────────────
    Label:
        text: 'Resultados'
        font_size: dp(13)
        bold: True
        color: 0.28, 0.30, 0.42, 1
        size_hint_y: None
        height: dp(22)
        halign: 'left'
        text_size: self.width, self.height
        valign: 'bottom'

    # ── Results scroll ────────────────────────────────────────
    ScrollView:
        do_scroll_x: False
        bar_width: dp(3)
        bar_color: 0.5, 0.6, 0.8, 0.6

        GridLayout:
            id: results_grid
            cols: 1
            spacing: dp(6)
            size_hint_y: None
            height: self.minimum_height
            padding: [0, 0, 0, dp(6)]
'''


def round2(x: float) -> float:
    """Arredondamento oficial Receita Federal: meia-unidade arredonda pra cima."""
    return float(Decimal(str(x)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))


def fmt_brl(amount: float) -> str:
    """Format a number as Brazilian Real (R$ 1.234,56)."""
    sign = '-' if amount < 0 else ''
    formatted = f'{abs(amount):,.2f}'                        # US: 1,234.56
    formatted = formatted.replace(',', 'X').replace('.', ',').replace('X', '.')  # BR: 1.234,56
    return f'{sign}R$ {formatted}'


# ──────────────────────────────────────────────────────────────────────────────
class InputRow(BoxLayout):
    index_label = StringProperty('#1')

    def __init__(self, index: int, change_cb, remove_cb, **kwargs):
        super().__init__(**kwargs)
        self._change_cb = change_cb
        self._remove_cb = remove_cb
        self.set_index(index)

    def set_index(self, index: int):
        self.index_label = f'#{index}'

    def on_value_changed(self, text: str):
        self._change_cb()

    def do_remove(self):
        self._remove_cb(self)

    def get_value(self) -> float:
        text = self.ids.txt.text.strip().replace(',', '.')
        try:
            return float(text)
        except ValueError:
            return 0.0


# ──────────────────────────────────────────────────────────────────────────────
class ResultCard(BoxLayout):
    card_title = StringProperty('')
    card_value = StringProperty('R$ 0,00')
    bg_color   = ListProperty([1, 1, 1, 1])
    lbl_color  = ListProperty([0.38, 0.38, 0.48, 1])
    val_color  = ListProperty([0.10, 0.10, 0.16, 1])

    def __init__(self, title: str, bg, lbl, val, **kwargs):
        super().__init__(**kwargs)
        self.card_title = title
        self.bg_color   = bg
        self.lbl_color  = lbl
        self.val_color  = val

    def update(self, amount: float):
        self.card_value = fmt_brl(amount)


# ──────────────────────────────────────────────────────────────────────────────
class MainScreen(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._rows  = []
        self._cards = {}
        # Defer init so that self.ids is populated after KV rules are applied
        Clock.schedule_once(self._init, 0)

    def _init(self, *_):
        self._build_result_cards()
        self.add_input()

    def _build_result_cards(self):
        # (key, title, bg_color, lbl_color, val_color)
        cfg = [
            ('lucro_bruto',    'Lucro Bruto',                  [0.95, 0.97, 1.00, 1], [0.13, 0.32, 0.68, 1], [0.09, 0.25, 0.58, 1]),
            ('pro_lab_bruto',  'Pró-labore Bruto  (28%)',      [0.94, 1.00, 0.96, 1], [0.09, 0.42, 0.26, 1], [0.06, 0.34, 0.20, 1]),
            ('inss',           'INSS  (11% do Pró-labore)',    [1.00, 0.97, 0.92, 1], [0.54, 0.36, 0.08, 1], [0.46, 0.28, 0.04, 1]),
            ('pro_lab_liq',    'Pró-labore Líquido',           [0.94, 1.00, 0.96, 1], [0.09, 0.42, 0.26, 1], [0.06, 0.34, 0.20, 1]),
            ('das',            'DAS  (6%)',                    [1.00, 0.97, 0.92, 1], [0.54, 0.36, 0.08, 1], [0.46, 0.28, 0.04, 1]),
            ('total_imp',      'Total de Impostos',            [1.00, 0.93, 0.93, 1], [0.62, 0.18, 0.18, 1], [0.54, 0.12, 0.12, 1]),
            ('dist_lucros',    'Distribuição de Lucros',       [0.93, 0.96, 1.00, 1], [0.16, 0.38, 0.65, 1], [0.11, 0.30, 0.57, 1]),
            ('total_pf',       'Total na Conta PF',            [0.93, 1.00, 0.95, 1], [0.11, 0.48, 0.28, 1], [0.07, 0.40, 0.22, 1]),
        ]
        for key, title, bg, lbl, val in cfg:
            card = ResultCard(title=title, bg=bg, lbl=lbl, val=val)
            self.ids.results_grid.add_widget(card)
            self._cards[key] = card

    # ── Input management ──────────────────────────────────────────────────────

    def add_input(self):
        if len(self._rows) >= 10:
            return
        idx = len(self._rows) + 1
        row = InputRow(index=idx, change_cb=self.recalculate, remove_cb=self._remove_row)
        self._rows.append(row)
        self.ids.inputs_grid.add_widget(row)
        self._refresh_state()
        self.recalculate()

    def _remove_row(self, row: InputRow):
        if len(self._rows) <= 1:
            # Keep at least one input — just clear its value
            row.ids.txt.text = ''
            return
        self._rows.remove(row)
        self.ids.inputs_grid.remove_widget(row)
        # Re-number remaining rows
        for i, r in enumerate(self._rows):
            r.set_index(i + 1)
        self._refresh_state()
        self.recalculate()

    def _refresh_state(self):
        n = len(self._rows)
        self.ids.counter_lbl.text = f'{n}/10'
        can_add = n < 10
        self.ids.add_btn.disabled = not can_add
        self.ids.add_btn.background_color = (
            [0.12, 0.56, 0.40, 1] if can_add else [0.58, 0.60, 0.62, 1]
        )

    # ── Calculations ──────────────────────────────────────────────────────────

    def recalculate(self, *_):
        lucro_bruto   = sum(r.get_value() for r in self._rows)  # exato
        pro_lab_bruto = round2(lucro_bruto * 0.28)
        inss          = round2(pro_lab_bruto * 0.11)  # imposto: arredonda pra cima
        das           = round2(lucro_bruto * 0.06)    # imposto: arredonda pra cima
        total_imp     = inss + das
        pro_lab_liq   = pro_lab_bruto - inss         # derivado dos valores já arredondados
        dist_lucros   = lucro_bruto - pro_lab_bruto - das
        total_pf      = pro_lab_liq + dist_lucros    # = lucro_bruto - total_imp ✓

        self._cards['lucro_bruto'].update(lucro_bruto)
        self._cards['pro_lab_bruto'].update(pro_lab_bruto)
        self._cards['inss'].update(inss)
        self._cards['pro_lab_liq'].update(pro_lab_liq)
        self._cards['das'].update(das)
        self._cards['total_imp'].update(total_imp)
        self._cards['dist_lucros'].update(dist_lucros)
        self._cards['total_pf'].update(total_pf)


# ──────────────────────────────────────────────────────────────────────────────
class FinanceApp(App):
    title = 'Calculadora Financeira'

    def build(self):
        Builder.load_string(KV)
        return MainScreen()


if __name__ == '__main__':
    FinanceApp().run()
