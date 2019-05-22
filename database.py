from datetime import datetime

from pony.orm import Database, Required, Optional, LongStr, Set, composite_key, sql_debug


db = Database('sqlite', 'singing_practice_log.sqlite', create_db=True)


# TODO: think of ON DELETE
# TODO: sensible __str__ for each entity?
# TODO: what to do with timezones? just use local time?


class PracticeSession(db.Entity):

    start = Required(datetime)
    notes = Optional(LongStr)
    exercises = Set('Exercise2PracticeSession')
    songs = Set('Song2PracticeSession')
    achievements = Set('Achievement2PracticeSession')
    light_bulb_moments = Set('LightBulbMoment')


class Category(db.Entity):

    name = Required(str, unique=True)
    exercises = Set('Exercise')

    def __str__(self):
        return self.name


class Exercise(db.Entity):

    name = Required(str, unique=True)
    category = Required('Category')
    practice_sessions = Set('Exercise2PracticeSession')

    def __str__(self):
        return f'{self.category.name}: {self.name}'


class Exercise2PracticeSession(db.Entity):

    session = Required(PracticeSession)
    exercise = Required(Exercise)
    how_it_felt = Optional(int)
    comment = Optional(str)


class Song(db.Entity):

    artist = Optional(str)
    title = Required(str)
    composite_key(artist, title)
    practice_sessions = Set('Song2PracticeSession')

    def __str__(self):
        return f'{self.artist} - {self.title}' if self.artist else self.title


class Song2PracticeSession(db.Entity):

    session = Required(PracticeSession)
    song = Required(Song)
    how_it_felt = Optional(int)
    comment = Optional(str)


class Achievement(db.Entity):

    name = Required(str, unique=True)
    unit = Optional(str)
    practice_sessions = Set('Achievement2PracticeSession')

    def __str__(self):
        return f'{self.name} ({self.unit})' if self.unit else self.name


class Achievement2PracticeSession(db.Entity):

    session = Required(PracticeSession)
    achievement = Required(Achievement)
    value = Required(int)


class LightBulbMoment(db.Entity):

    session = Required(PracticeSession)
    effect = Required(str)
    clue = Required(str)


sql_debug(True)
db.generate_mapping(create_tables=True)
