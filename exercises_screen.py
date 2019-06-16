from PySide2 import QtWidgets, QtCore

from exercises_controller import ExercisesController
from practice_log_controller import PracticeLogController
from practice_log_screen import PracticeLogScreen
from widgets import AddExerciseDialog, LayoutWithTable


class SingleExerciseScreen(QtWidgets.QDialog):

    def __init__(self, exercise_name, sessions_for_exercise, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.table = LayoutWithTable(
            label_text=exercise_name,
            add_action=None,
            table_headers=['date', 'how it felt?', 'comment'],
            table_content=sessions_for_exercise,
            row_action=self.show_practice_log_screen,
        )
        self.setLayout(self.table)

    def show_practice_log_screen(self, practice_session_id):
        screen = PracticeLogScreen(
            practice_log_controller=PracticeLogController(practice_session_id),
            parent=self,
        )
        screen.show()


class ExercisesListScreen(QtWidgets.QWidget):

    def __init__(self, exercises_controller: ExercisesController, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.exercises_controller = exercises_controller

        self.table = LayoutWithTable(
            label_text='exercises',
            add_action=self.add_exercise,
            table_headers=['category', 'name', 'last done', 'times done'],
            table_content=self.exercises_controller.get_exercises(),
            row_action=self.show_single_exercise_screen,
        )
        # TODO: filters/sorting in table
        self.setLayout(self.table)

    def add_exercise(self):
        categories = self.exercises_controller.get_existing_categories()
        dialog = AddExerciseDialog(categories=categories, parent=self)
        dialog.show()

        if dialog.exec_():
            data = dialog.get_data()
            self.exercises_controller.add_exercise(**data)
            # TODO: refresh the table to show newly added exercise

    def show_single_exercise_screen(self, exercise_id):
        screen = SingleExerciseScreen(
            exercise_name=self.exercises_controller.get_exercise_string(exercise_id),
            sessions_for_exercise=self.exercises_controller.get_sessions_for_exercise(exercise_id),
            parent=self,
        )
        screen.show()


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = ExercisesListScreen(exercises_controller=ExercisesController())
    window.show()

    sys.exit(app.exec_())
