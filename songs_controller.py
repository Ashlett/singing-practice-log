from database import Song
from list_controller import ListController


class SongsController(ListController):

    entity = Song

    def get_extra_keys(self, item):
        return {'artist': item.artist, 'title': item.title}
