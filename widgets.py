from PySide2 import QtWidgets
from PySide2.QtCore import Qt


HOW_IT_FELT_EMOTICONS = {None: '', 3: '😃', 2: '😐', 1: '😞'}


class DataWidget:

    def __init__(self, gui_label, data_label):
        self.gui_label = gui_label
        self.data_label = data_label

    def get_data(self):
        raise NotImplementedError


class ChoicesWidget(DataWidget):

    def __init__(self, gui_label, data_label, choices: dict):
        super().__init__(gui_label, data_label)

        self.widget = QtWidgets.QComboBox()
        for data, label in choices.items():
            self.widget.addItem(label, userData=data)

    def get_data(self):
        return self.widget.currentData()


class TextWidget(DataWidget):

    def __init__(self, gui_label, data_label):
        super().__init__(gui_label, data_label)

        self.widget = QtWidgets.QLineEdit()

    def get_data(self):
        return self.widget.text()


class TextWidgetWithAutocomplete(TextWidget):

    def __init__(self, gui_label, data_label, word_list):
        super().__init__(gui_label, data_label)

        completer = QtWidgets.QCompleter(word_list)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.widget.setCompleter(completer)


class IntegerWidget(DataWidget):

    def __init__(self, gui_label, data_label):
        super().__init__(gui_label, data_label)

        self.widget = QtWidgets.QSpinBox()

    def get_data(self):
        return self.widget.value()


class AddEntityDialog(QtWidgets.QDialog):

    def init_layout(self):
        full_layout = QtWidgets.QVBoxLayout()

        for w in self.data_widgets:
            layout = QtWidgets.QHBoxLayout()
            layout.addWidget(QtWidgets.QLabel(w.gui_label))
            layout.addWidget(w.widget)
            full_layout.addLayout(layout)

        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        full_layout.addWidget(button_box)

        self.setLayout(full_layout)

    def get_data(self):
        return {w.data_label: w.get_data() for w in self.data_widgets}


class AddExerciseDialog(AddEntityDialog):

    def __init__(self, categories, parent=None):
        super().__init__(parent)

        self.data_widgets = (
            TextWidgetWithAutocomplete('category', 'category_name', word_list=categories),
            TextWidget('name', 'name'),
        )
        self.init_layout()


class AddExerciseToSessionDialog(AddEntityDialog):

    def __init__(self, exercise_choices, parent=None):
        super().__init__(parent)

        self.data_widgets = (
            ChoicesWidget('exercise', 'exercise', choices=exercise_choices),
            ChoicesWidget('how it felt?', 'how_it_felt', choices=HOW_IT_FELT_EMOTICONS),
            TextWidget('comment', 'comment'),
        )
        self.init_layout()


class AddSongToSessionDialog(AddEntityDialog):

    def __init__(self, artists, titles, parent=None):
        super().__init__(parent)

        self.data_widgets = (
            TextWidgetWithAutocomplete('artist', 'artist', word_list=artists),
            TextWidgetWithAutocomplete('title', 'title', word_list=titles),
            ChoicesWidget('how it felt?', 'how_it_felt', choices=HOW_IT_FELT_EMOTICONS),
            TextWidget('comment', 'comment'),
        )
        self.init_layout()


class AddAchievementToSessionDialog(AddEntityDialog):

    def __init__(self, achievement_choices, parent=None):
        super().__init__(parent)

        self.data_widgets = (
            ChoicesWidget('achievement', 'achievement', choices=achievement_choices),
            IntegerWidget('value', 'value')
        )
        self.init_layout()


class AddLightBulbMomentDialog(AddEntityDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.data_widgets = (
            TextWidget('effect', 'effect'),
            TextWidget('clue', 'clue'),
        )
        self.init_layout()


class LayoutWithTable(QtWidgets.QVBoxLayout):

    def __init__(self, label_text, add_action, table_headers, table_content, row_action=None):
        super().__init__()
        self.rows_to_ids = {}
        self.row_action = row_action

        label = QtWidgets.QLabel(label_text)
        self.addWidget(label)

        if add_action:
            add_button = QtWidgets.QPushButton('+')
            self.addWidget(add_button)
            add_button.clicked.connect(add_action)

        if table_content:
            table = QtWidgets.QTableWidget(len(table_content), len(table_headers))
            table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            table.setHorizontalHeaderLabels(table_headers)
            for r, data in enumerate(table_content):
                if row_action:
                    self.rows_to_ids[r] = data['id']
                for c, header in enumerate(table_headers):
                    item = data[header]
                    if header == 'how it felt?':
                        item = HOW_IT_FELT_EMOTICONS[item]
                    table.setItem(r, c, QtWidgets.QTableWidgetItem(item))
            if row_action:
                table.cellDoubleClicked.connect(self.cell_double_clicked)
            self.addWidget(table)

    def cell_double_clicked(self, row, column):
        action_id = self.rows_to_ids[row]
        self.row_action(action_id)


class SingleItemScreen(QtWidgets.QDialog):

    def __init__(self, item_name, sessions_for_item, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.table = LayoutWithTable(
            label_text=item_name,
            add_action=None,
            table_headers=['date', 'how it felt?', 'comment'],
            table_content=sessions_for_item,
            row_action=self.show_practice_log_screen,
        )
        self.setLayout(self.table)

    def show_practice_log_screen(self, practice_session_id):
        from practice_log_controller import PracticeLogController
        from practice_log_screen import PracticeLogScreen

        screen = PracticeLogScreen(
            practice_log_controller=PracticeLogController(practice_session_id),
            parent=self,
        )
        screen.show()
