from PySide2 import QtWidgets, QtCore

from songs_controller import SongsController
from practice_log_controller import PracticeLogController
from practice_log_screen import PracticeLogScreen
from widgets import LayoutWithTable


class SingleSongScreen(QtWidgets.QDialog):

    def __init__(self, song_name, sessions_for_song, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.table = LayoutWithTable(
            label_text=song_name,
            add_action=None,
            table_headers=['date', 'how it felt?', 'comment'],
            table_content=sessions_for_song,
            row_action=self.show_practice_log_screen,
        )
        self.setLayout(self.table)

    def show_practice_log_screen(self, practice_session_id):
        screen = PracticeLogScreen(
            practice_log_controller=PracticeLogController(practice_session_id),
            parent=self,
        )
        screen.show()


class SongsListScreen(QtWidgets.QWidget):

    def __init__(self, songs_controller: SongsController, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.songs_controller = songs_controller

        self.table = LayoutWithTable(
            label_text='songs',
            add_action=None,
            table_headers=['artist', 'title', 'last done', 'times done'],
            table_content=self.songs_controller.get_all_items(),
            row_action=self.show_single_song_screen,
        )
        # TODO: filters/sorting in table
        self.setLayout(self.table)

    def show_single_song_screen(self, song_id):
        screen = SingleSongScreen(
            song_name=self.songs_controller.get_item_string(song_id),
            sessions_for_song=self.songs_controller.get_sessions_for_item(song_id),
            parent=self,
        )
        screen.show()


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = SongsListScreen(songs_controller=SongsController())
    window.show()

    sys.exit(app.exec_())
