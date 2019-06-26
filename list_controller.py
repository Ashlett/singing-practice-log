from pony.orm import db_session, max


class ListController:

    entity = None

    @db_session
    def get_all_items(self):
        items = []
        for item in self.entity.select():
            if item.practice_sessions:
                last_done = max(e2ps.session.start for e2ps in item.practice_sessions).strftime('%Y-%m-%d')
            else:
                last_done = ''
            data = {
                'id': item.id,
                'last done': last_done,
                'times done': str(len(item.practice_sessions)),
            }
            data.update(self.get_extra_keys(item))
            items.append(data)
        return items

    def get_extra_keys(self, item):
        return {}

    @db_session
    def get_item_string(self, item_id):
        item = self.entity[item_id]
        return str(item)

    @db_session
    def get_sessions_for_item(self, item_id):
        item = self.entity[item_id]
        practice_sessions = []
        for ps in item.practice_sessions:
            practice_sessions.append({
                'id': ps.session.id,
                'date': ps.session.start.strftime('%Y-%m-%d %H:%M'),
                'how it felt?': ps.how_it_felt,
                'comment': ps.comment,
            })
        practice_sessions.sort(key=lambda x: x['date'], reverse=True)
        return practice_sessions
