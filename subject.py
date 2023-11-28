from enum import Enum, auto

class Day(Enum):
    MONDAY = auto()
    TUESDAY = auto()
    WEDNESDAY = auto()
    THURSDAY = auto()
    FRIDAY = auto()

class Semester(Enum):
    FIRST = auto()
    SECOND = auto()

class Subject:
    day: Day
    indexes: list[int]
    name: str
    years: int
    semester: Semester

    def __init__(self, day: Day, indexes: list[int], name: str, years: int, semester: Semester):
        self.day = day
        self.indexes = indexes
        self.name = name
        self.years = years
        self.semester = semester

def filter_subjects(roles: list[str]) -> list[Subject]:
    subjects = []
    for role in roles:
        if role.count(':') != 2:
            continue

        a, b, c = role.split(':')

        day = get_day(a[0])
        indexes = list(map(int, a[1:].split(',')))
        name = b
        years = int(c[:-3])
        semester = get_semester(c[-3:])

        subject = Subject(day, indexes, name, years, semester)
        subjects.append(subject)
    return subjects

def get_day(day: str) -> Day:
    match day:
        case '月':
            return Day.MONDAY
        case '火':
            return Day.TUESDAY
        case '水':
            return Day.WEDNESDAY
        case '木':
            return Day.THURSDAY
        case '金':
            return Day.FRIDAY

def get_semester(semester: str) -> Semester:
    match semester:
        case '前学期':
            return Semester.FIRST
        case '後学期':
            return Semester.SECOND
