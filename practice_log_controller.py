from pony.orm import db_session

from database import PracticeSession, Exercise2PracticeSession


class PracticeLogController:

    def __init__(self, practice_session: PracticeSession):
        self.practice_session = practice_session

    def get_exercises(self):
        return self.practice_session.exercises

    @db_session
    def add_exercise(self, data):
        Exercise2PracticeSession(session=self.practice_session.id, **data)

    def get_songs(self):
        return self.practice_session.songs

