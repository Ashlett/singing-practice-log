from PySide2 import QtWidgets

from light_bulb_moments_controller import LightBulbMomentsController
from widgets import LayoutWithTable


class LightBulbMomentsScreen(QtWidgets.QWidget):

    def __init__(self, controller: LightBulbMomentsController, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.controller = controller

        self.table = LayoutWithTable(
            label_text='light bulb moments',
            table_headers=['date', 'effect', 'clue'],
            table_content=self.controller.get_all_items(),
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


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = LightBulbMomentsScreen(controller=LightBulbMomentsController())
    window.show()

    sys.exit(app.exec_())
