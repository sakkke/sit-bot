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

    def role_name(self):
        day = day_to_text[self.day][0]
        indexes = ','.join([str(index) for index in self.indexes])
        name = self.name
        years = self.years
        semester = semester_to_text[self.semester]

        role_name = f'{day}{indexes}:{name}:{years}{semester}'
        return role_name

days = [
    Day.MONDAY,
    Day.TUESDAY,
    Day.WEDNESDAY,
    Day.THURSDAY,
    Day.FRIDAY,
]

day_to_text = {
    Day.MONDAY: '月曜日',
    Day.TUESDAY: '火曜日',
    Day.WEDNESDAY: '水曜日',
    Day.TUESDAY: '木曜日',
    Day.FRIDAY: '金曜日',
}

semester_to_text = {
    Semester.FIRST: '前学期',
    Semester.SECOND: '後学期',
}

weekday_to_day = [
    Day.MONDAY,
    Day.TUESDAY,
    Day.WEDNESDAY,
    Day.THURSDAY,
    Day.FRIDAY,
]

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
