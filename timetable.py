from subject import Day, Semester, Subject

def get_timetable(subjects: list[Subject], years: int, semester: Semester):
    timetable = {
        '月曜日': [' '] * 5,
        '火曜日': [' '] * 5,
        '水曜日': [' '] * 5,
        '木曜日': [' '] * 5,
        '金曜日': [' '] * 5,
    }
    day_to_text = {
        Day.MONDAY: '月曜日',
        Day.TUESDAY: '火曜日',
        Day.WEDNESDAY: '水曜日',
        Day.THURSDAY: '木曜日',
        Day.FRIDAY: '金曜日',
    }
    chunk_size = 8
    for subject in subjects:
        if subject.years != years or subject.semester != semester:
            continue

        day = day_to_text[subject.day]
        name = '\n'.join([subject.name[i:i+chunk_size] for i in range(0, len(subject.name), chunk_size)])
        for index in subject.indexes:
            timetable[day][index - 1] = name
    return timetable
