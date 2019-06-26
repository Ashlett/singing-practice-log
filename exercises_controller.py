from pony.orm import db_session, select

from database import Category, Exercise
from list_controller import ListController


class ExercisesController(ListController):

    entity = Exercise

    def get_extra_keys(self, item):
        return {'category': str(item.category), 'name': item.name}

    @db_session
    def get_existing_categories(self):
        return list(select(c.name for c in Category))

    @db_session
    def add_exercise(self, category_name, name):
        category = Category.get(name=category_name)
        if not category:
            category = Category(name=category_name)
        Exercise(category=category, name=name)
