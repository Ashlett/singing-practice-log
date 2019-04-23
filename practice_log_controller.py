from pony.orm import db_session

from database import PracticeSession, Exercise, Exercise2PracticeSession


class PracticeLogController:

    def __init__(self, practice_session_id:int):
        self.practice_session_id = practice_session_id

    @db_session
    def get_exercise_choices(self):
        exercise_choices = []
        for e in Exercise.select():
            exercise_choices.append({
                'label': str(e),
                'id': e.id,
            })
        return exercise_choices

    @db_session
    def get_exercises(self):
        exercises = []
        practice_session = PracticeSession[self.practice_session_id]
        for exercise in practice_session.exercises:
            exercises.append({
                'name': exercise.exercise.name,
                'category': exercise.exercise.category.name,
                'how it felt?': exercise.how_it_felt,
                'comment': exercise.comment,
            })
        return exercises

    @db_session
    def add_exercise(self, data):
        Exercise2PracticeSession(session=self.practice_session_id, **data)

    @db_session
    def get_songs(self):
        songs = []
        practice_session = PracticeSession[self.practice_session_id]
        for song in practice_session.songs:
            songs.append({
                'artist': song.song.artist,
                'title': song.song.title,
                'how it felt?': song.how_it_felt,
                'comment': song.comment,
            })
        return songs
