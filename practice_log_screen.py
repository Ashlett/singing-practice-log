from PySide2 import QtWidgets
from PySide2.QtCore import Qt

from practice_log_controller import PracticeLogController


HOW_IT_FELT_EMOTICONS = {None: '', 3: '😃', 2: '😐', 1: '😞'}


def make_layout_with_label(widget, label_text):
    """Takes a widget and label text, returns a horizontal layout with label + widget"""
    layout = QtWidgets.QHBoxLayout()
    layout.addWidget(QtWidgets.QLabel(label_text))
    layout.addWidget(widget)
    return layout


class AddExerciseDialog(QtWidgets.QDialog):

    def __init__(self, exercise_choices, parent=None):
        super().__init__(parent)

        self.exercise = QtWidgets.QComboBox()
        for e in exercise_choices:
            self.exercise.addItem(e['label'], userData=e['id'])

        self.how_it_felt = QtWidgets.QComboBox()
        for num, face in HOW_IT_FELT_EMOTICONS.items():
            self.how_it_felt.addItem(face, userData=num)

        self.comment = QtWidgets.QLineEdit()

        widgets_and_labels = (
            (self.exercise, 'exercise'),
            (self.how_it_felt, 'how it felt?'),
            (self.comment, 'comment'),
        )

        full_layout = QtWidgets.QVBoxLayout()
        for widget, label in widgets_and_labels:
            layout = make_layout_with_label(widget=widget, label_text=label)
            full_layout.addLayout(layout)

        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        full_layout.addWidget(button_box)

        self.setLayout(full_layout)

    def get_data(self):
        return {
            'exercise': self.exercise.currentData(),
            'how_it_felt': self.how_it_felt.currentData(),
            'comment': self.comment.text(),
        }


class AddSongDialog(QtWidgets.QDialog):

    def __init__(self, artists, titles, parent=None):
        super().__init__(parent)

        self.artist = QtWidgets.QLineEdit()
        completer = QtWidgets.QCompleter(artists, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.artist.setCompleter(completer)

        self.title = QtWidgets.QLineEdit()
        completer = QtWidgets.QCompleter(titles, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.title.setCompleter(completer)

        self.how_it_felt = QtWidgets.QComboBox()
        for num, face in HOW_IT_FELT_EMOTICONS.items():
            self.how_it_felt.addItem(face, userData=num)

        self.comment = QtWidgets.QLineEdit()

        widgets_and_labels = (
            (self.artist, 'artist'),
            (self.title, 'title'),
            (self.how_it_felt, 'how it felt?'),
            (self.comment, 'comment'),
        )

        full_layout = QtWidgets.QVBoxLayout()
        for widget, label in widgets_and_labels:
            layout = make_layout_with_label(widget=widget, label_text=label)
            full_layout.addLayout(layout)

        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        full_layout.addWidget(button_box)

        self.setLayout(full_layout)

    def get_data(self):
        return {
            'artist': self.artist.text(),
            'title': self.title.text(),
            'how_it_felt': self.how_it_felt.currentData(),
            'comment': self.comment.text(),
        }


class LayoutWithTable(QtWidgets.QVBoxLayout):

    def __init__(self, label_text, add_action, table_headers, table_content):
        super().__init__()

        label = QtWidgets.QLabel(label_text)
        self.addWidget(label)
        add_button = QtWidgets.QPushButton('+')
        self.addWidget(add_button)

        if add_action:
            add_button.clicked.connect(add_action)

        if table_content:
            table = QtWidgets.QTableWidget(len(table_content), len(table_headers))
            table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            table.setHorizontalHeaderLabels(table_headers)
            for r, data in enumerate(table_content):
                for c, header in enumerate(table_headers):
                    item = data[header]
                    if header == 'how it felt?':
                        item = HOW_IT_FELT_EMOTICONS[item]
                    table.setItem(r, c, QtWidgets.QTableWidgetItem(item))
            self.addWidget(table)


class PracticeLogScreen(QtWidgets.QWidget):

    def __init__(self, practice_log_controller: PracticeLogController, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.practice_log_controller = practice_log_controller
        self.init_layouts()

    def init_layouts(self):
        self.layouts = [
            self.init_time_layout(),
            LayoutWithTable(
                label_text='exercises',
                add_action=self.add_exercise,
                table_headers=['name', 'category', 'how it felt?', 'comment'],
                table_content=self.practice_log_controller.get_exercises(),
            ),
            LayoutWithTable(
                label_text='songs',
                add_action=self.add_song,
                table_headers=['artist', 'title', 'how it felt?', 'comment'],
                table_content=self.practice_log_controller.get_songs(),
            ),
            LayoutWithTable(
                label_text='achievements',
                add_action=self.add_achievement,
                table_headers=['name', 'value', 'unit'],
                table_content=self.practice_log_controller.get_achievements(),
            ),
            LayoutWithTable(
                label_text='light bulb moments',
                add_action=self.add_light_bulb_moment,
                table_headers=['effect', 'clue'],
                table_content=self.practice_log_controller.get_light_bulb_moments(),
            ),
            self.init_notes_layout(),
        ]
        full_layout = QtWidgets.QVBoxLayout()
        for i, layout in enumerate(self.layouts):
            full_layout.addLayout(layout, i)
        self.setLayout(full_layout)

    def init_time_layout(self):
        self.time_picker = QtWidgets.QDateTimeEdit()
        self.time_picker.setDateTime(self.practice_log_controller.get_start())
        self.time_picker.setCalendarPopup(True)
        save_start_button = QtWidgets.QPushButton('Save start time')
        save_start_button.clicked.connect(self.save_start)

        time_layout = QtWidgets.QHBoxLayout()
        time_layout.addWidget(QtWidgets.QLabel('start'))
        time_layout.addWidget(self.time_picker)
        time_layout.addWidget(save_start_button)

        return time_layout

    def save_start(self):
        new_time = self.time_picker.dateTime().toPython()
        self.practice_log_controller.save_start(start=new_time)

    def init_notes_layout(self):
        self.notes = QtWidgets.QTextEdit()
        self.notes.insertPlainText(self.practice_log_controller.get_notes())
        # TODO: button active only if notes changed?
        save_notes_button = QtWidgets.QPushButton('Save notes')
        save_notes_button.clicked.connect(self.save_notes)
        notes_layout = QtWidgets.QVBoxLayout()
        notes_layout.addWidget(QtWidgets.QLabel('notes'))
        notes_layout.addWidget(self.notes)
        notes_layout.addWidget(save_notes_button)
        return notes_layout

    def save_notes(self):
        new_notes = self.notes.toPlainText()
        self.practice_log_controller.save_notes(new_notes)

    def add_exercise(self):
        exercise_choices = self.practice_log_controller.get_exercise_choices()
        # TODO: error dialog if no exercises to select from
        dialog = AddExerciseDialog(exercise_choices=exercise_choices, parent=self)
        dialog.show()

        if dialog.exec_():
            data = dialog.get_data()
            self.practice_log_controller.add_exercise(data=data)
            # TODO: refresh the table to show newly added exercise

    def add_song(self):
        dialog = AddSongDialog(
            artists=self.practice_log_controller.get_existing_artists(),
            titles=self.practice_log_controller.get_existing_titles(),
            parent=self,
        )
        dialog.show()

        if dialog.exec_():
            data = dialog.get_data()
            self.practice_log_controller.add_song(**data)
            # TODO: refresh the table to show newly added song

    def add_achievement(self):
        # TODO
        pass

    def add_light_bulb_moment(self):
        # TODO
        pass


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = PracticeLogScreen(practice_log_controller=PracticeLogController(1))
    window.show()

    sys.exit(app.exec_())
