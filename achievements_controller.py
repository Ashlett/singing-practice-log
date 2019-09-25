from pony.orm import db_session, max

from database import Achievement
from list_controller import ListController


class AchievementsController(ListController):

    entity = Achievement

    def get_extra_keys(self, item):
        best_result = str(max(e2ps.value for e2ps in item.practice_sessions)) if item.practice_sessions else ''
        return {
            'name': item.name,
            'unit': item.unit,
            'best result': best_result,
        }

    def get_extra_keys_for_session(self, ps):
        return {'value': str(ps.value)}

    @db_session
    def add_achievement(self, name, unit):
        Achievement(name=name, unit=unit)
