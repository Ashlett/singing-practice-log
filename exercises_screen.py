from PySide2 import QtWidgets

from exercises_controller import ExercisesController
from widgets import AddExerciseDialog, LayoutWithTable


class ExercisesListScreen(QtWidgets.QWidget):

    def __init__(self, exercises_controller: ExercisesController, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.exercises_controller = exercises_controller

        self.table = LayoutWithTable(
            label_text='exercises',
            add_action=self.add_exercise,
            table_headers=['category', 'name', 'last done', 'times done'],
            table_content=self.exercises_controller.get_exercises()
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


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = ExercisesListScreen(exercises_controller=ExercisesController())
    window.show()

    sys.exit(app.exec_())
