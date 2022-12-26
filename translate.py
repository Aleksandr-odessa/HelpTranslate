import sys
from PyQt6.QtWidgets import (QApplication,
                             QMainWindow,
                             QWidget,
                             QVBoxLayout,
                             QHBoxLayout,
                             QPushButton, QComboBox, QLabel)
from translate_ua import Translate
from in_out_word import InOut

dict_lang = {"text_in":"польский", "text_out":"украинский"}
dict_to_angl = {'украинский':'uk', 'русский':'ru','польский':'pl'}


def dict_language():
    in_ = dict_to_angl.get(dict_lang.get("text_in"))
    out_ = dict_to_angl.get(dict_lang.get("text_out"))
    ts = Translate(in_, out_, 'perevod.docx')
    text_in = ts.word_read()
    ts.translated(text_in)



# class of main widgets
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("App translate")
        layout_vert = QVBoxLayout()
        button_send = QPushButton('перевести')
        button_send.clicked.connect(dict_language)
        layout_vert.addWidget(button_send)
        layout_hor = QHBoxLayout()
        combo_in = Combo(50,50,layout_hor)
        in_ = combo_in.combo()
        in_.textActivated.connect(combo_in.on_activated_in)
        combo_out = Combo(100,50,layout_hor)
        out_ = combo_out.combo()
        out_.textActivated.connect(combo_out.on_activated_out)
        layout_vert.addLayout(layout_hor)
        out_.setCurrentIndex(2)
        widget = QWidget()
        widget.setLayout(layout_vert)
        self.setCentralWidget(widget)
        self.setGeometry(300, 300, 300, 200)


# class of widget for selecting language
class Combo:

    def __init__(self, x,y, layout):
        self.x = x
        self.y = y
        self.layout = layout

    def combo(self):
        language = ["польский", "русский", "украинский"]
        combo = QComboBox()
        self.layout.addWidget(combo)
        combo.addItems(language)
        combo.move(self.x, self.y)
        return combo

    # metod of transmisions selecting start language from QBox to dictionary
    @staticmethod
    def on_activated_in(text):
        dict_lang["text_in"] = text

    # method of transmission selecting finish language from QBox to dictionary
    @staticmethod
    def on_activated_out(text):
        dict_lang["text_out"] = text

def main_windows():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

main_windows()