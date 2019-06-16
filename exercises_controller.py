from pony.orm import db_session, max, select

from database import Category, Exercise


class ExercisesController:

    @db_session
    def get_exercises(self):
        exercises = []
        for e in Exercise.select():
            if e.practice_sessions:
                last_done = max(e2ps.session.start for e2ps in e.practice_sessions).strftime('%Y-%m-%d')
            else:
                last_done = ''
            exercises.append({
                'category': str(e.category),
                'name': e.name,
                'last done': last_done,
                'times done': str(len(e.practice_sessions)),
            })
        return exercises

    @db_session
    def get_existing_categories(self):
        return list(select(c.name for c in Category))

    @db_session
    def add_exercise(self, category_name, name):
        category = Category.get(name=category_name)
        if not category:
            category = Category(name=category_name)
        Exercise(category=category, name=name)
