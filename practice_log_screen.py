from PySide2 import QtWidgets

from widgets import (
    AddAchievementToSessionDialog, AddExerciseToSessionDialog, AddLightBulbMomentDialog, AddSongToSessionDialog,
    LayoutWithTable
)
from practice_log_controller import PracticeLogController


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
        dialog = AddExerciseToSessionDialog(exercise_choices=exercise_choices, parent=self)
        dialog.show()

        if dialog.exec_():
            data = dialog.get_data()
            self.practice_log_controller.add_exercise(data=data)
            # TODO: refresh the table to show newly added exercise

    def add_song(self):
        dialog = AddSongToSessionDialog(
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
        achievement_choices = self.practice_log_controller.get_achievement_choices()
        dialog = AddAchievementToSessionDialog(achievement_choices=achievement_choices, parent=self)
        dialog.show()

        if dialog.exec_():
            data = dialog.get_data()
            self.practice_log_controller.add_achievement(**data)

    def add_light_bulb_moment(self):
        dialog = AddLightBulbMomentDialog(self)
        dialog.show()

        if dialog.exec_():
            data = dialog.get_data()
            self.practice_log_controller.add_light_bulb_moment(**data)


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = PracticeLogScreen(practice_log_controller=PracticeLogController(1))
    window.show()

    sys.exit(app.exec_())
