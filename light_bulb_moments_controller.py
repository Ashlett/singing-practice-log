from pony.orm import db_session

from database import LightBulbMoment


class LightBulbMomentsController:

    @db_session
    def get_all_items(self):
        items = []
        for lbm in LightBulbMoment.select():
            data = {
                'id': lbm.session.id,
                'date': lbm.session.start.strftime('%Y-%m-%d %H:%M'),
                'effect': lbm.effect,
                'clue': lbm.clue,
            }
            items.append(data)
        return items
