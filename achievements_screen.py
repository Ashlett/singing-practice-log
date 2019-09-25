from PySide2 import QtWidgets

from achievements_controller import AchievementsController
from widgets import AddAchievementDialog, LayoutWithTable, SingleAchievementScreen


class AchievementsScreen(QtWidgets.QWidget):

    def __init__(self, controller: AchievementsController, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.controller = controller

        self.table = LayoutWithTable(
            label_text='achievements',
            add_action=self.add_achievement,
            table_headers=['name', 'unit', 'best result', 'last done', 'times done'],
            table_content=self.controller.get_all_items(),
            row_action=self.show_single_achievement_screen,
        )
        # TODO: filters/sorting in table
        self.setLayout(self.table)

    def add_achievement(self):
        dialog = AddAchievementDialog(parent=self)
        dialog.show()

        if dialog.exec_():
            data = dialog.get_data()
            self.controller.add_achievement(**data)
            # TODO: refresh the table to show newly added achievement

    def show_single_achievement_screen(self, achievement_id):
        screen = SingleAchievementScreen(
            item_name=self.controller.get_item_string(achievement_id),
            sessions_for_item=self.controller.get_sessions_for_item(achievement_id),
            parent=self,
        )
        screen.show()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = AchievementsScreen(controller=AchievementsController())
    window.show()

    sys.exit(app.exec_())
