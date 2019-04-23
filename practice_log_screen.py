from PySide2 import QtWidgets

from database import Exercise
from practice_log_controller import PracticeLogController


HOW_IT_FELT_EMOTICONS = {None: '', 3: '😃', 2: '😐', 1: '😞'}


def make_layout_with_label(widget, label_text):
    """Takes a widget and label text, returns a horizontal layout with label + widget"""
    layout = QtWidgets.QHBoxLayout()
    layout.addWidget(QtWidgets.QLabel(label_text))
    layout.addWidget(widget)
    return layout


class AddExerciseDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.exercise = QtWidgets.QComboBox()
        # TODO: separate DB from UI
        with db_session:
            if Exercise.select().count() == 0:
                # TODO: error dialog if no exercises to select from
                pass
            for e in Exercise.select():
                self.exercise.addItem(str(e), userData=e.id)

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


class PracticeLogScreen(QtWidgets.QWidget):

    def __init__(self, practice_log_controller: PracticeLogController, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.practice_log_controller = practice_log_controller
        self.init_layouts()

    def init_layouts(self):
        self.layouts = [
            self.init_time_layout(),
            self.init_exercises_layout(),
            self.init_songs_layout(),
        ]
        full_layout = QtWidgets.QVBoxLayout()
        for i, layout in enumerate(self.layouts):
            full_layout.addLayout(layout, i)
        self.setLayout(full_layout)

    def init_time_layout(self):
        time_label = QtWidgets.QLabel('time')
        self.time_picker = QtWidgets.QDateTimeEdit()
        self.time_picker.setCalendarPopup(True)

        time_layout = QtWidgets.QHBoxLayout()
        time_layout.addWidget(time_label)
        time_layout.addWidget(self.time_picker)

        return time_layout

    def init_exercises_layout(self):
        exercises_layout = QtWidgets.QVBoxLayout()

        exercises_label = QtWidgets.QLabel('exercises')
        exercises_layout.addWidget(exercises_label)
        add_exercise_button = QtWidgets.QPushButton('+')
        exercises_layout.addWidget(add_exercise_button)

        add_exercise_button.clicked.connect(self.add_exercise)

        exercises = self.practice_log_controller.get_exercises()
        if exercises:
            headers = ['name', 'category', 'how it felt?', 'comment']
            exercises_table = QtWidgets.QTableWidget(len(exercises), len(headers))
            exercises_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            exercises_table.setHorizontalHeaderLabels(headers)
            for r, exercise in enumerate(exercises):
                for c, item in enumerate((
                    exercise.exercise.name,
                    exercise.exercise.category.name,
                    HOW_IT_FELT_EMOTICONS[exercise.how_it_felt],
                    exercise.comment
                )):
                    exercises_table.setItem(r, c, QtWidgets.QTableWidgetItem(item))
            exercises_layout.addWidget(exercises_table)

        return exercises_layout

    def init_songs_layout(self):
        songs_layout = QtWidgets.QVBoxLayout()

        songs_label = QtWidgets.QLabel('songs')
        songs_layout.addWidget(songs_label)
        add_exercise_button = QtWidgets.QPushButton('+')
        songs_layout.addWidget(add_exercise_button)

        songs = self.practice_log_controller.get_songs()
        if songs:
            headers = ['artist', 'title', 'how it felt?', 'comment']
            exercises_table = QtWidgets.QTableWidget(len(songs), len(headers))
            exercises_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            exercises_table.setHorizontalHeaderLabels(headers)
            for r, song in enumerate(songs):
                for c, item in enumerate((
                    song.song.artist,
                    song.song.title,
                    HOW_IT_FELT_EMOTICONS[song.how_it_felt],
                    song.comment
                )):
                    exercises_table.setItem(r, c, QtWidgets.QTableWidgetItem(item))
            songs_layout.addWidget(exercises_table)

        return songs_layout

    def add_exercise(self):
        dialog = AddExerciseDialog(self)
        dialog.show()

        if dialog.exec_():
            data = dialog.get_data()
            print(data)
            self.practice_log_controller.add_exercise(data=data)


if __name__ == '__main__':

    import sys

    from pony.orm import db_session

    from database import PracticeSession

    with db_session():
        practice_session = PracticeSession.select().first()

        app = QtWidgets.QApplication(sys.argv)
        window = PracticeLogScreen(practice_log_controller=PracticeLogController(practice_session))
        window.show()

    sys.exit(app.exec_())
