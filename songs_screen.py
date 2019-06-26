from PySide2 import QtWidgets

from songs_controller import SongsController
from widgets import LayoutWithTable, SingleItemScreen


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
        screen = SingleItemScreen(
            item_name=self.songs_controller.get_item_string(song_id),
            sessions_for_item=self.songs_controller.get_sessions_for_item(song_id),
            parent=self,
        )
        screen.show()


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = SongsListScreen(songs_controller=SongsController())
    window.show()

    sys.exit(app.exec_())
