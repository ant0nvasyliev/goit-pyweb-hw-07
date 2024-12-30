from sqlalchemy import func, desc, select, and_

from conf.models import Grade, Teacher, Student, Group, Subject
from conf.db import session

# 1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_1():
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Student).join(Grade).group_by(Student.id).order_by(desc('average_grade')).limit(5).all()
    return result

# 2. Знайти студента із найвищим середнім балом з певного предмета.
def select_2(subject_id):
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Student).filter(Grade.subject_id == subject_id).group_by(Student.id).order_by(desc('average_grade')).limit(1).all()
    return result

# 3. Знайти середній бал у групах з певного предмета.
def select_3(subject_id):
    result = session.query(Group.name, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Student).join(Group).filter(Grade.subject_id == subject_id).group_by(Group.id).all()
    return result

# 4. Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4():
    result = session.query(func.round(func.avg(Grade.grade), 2).label('average_grade')).scalar()
    return result

# 5. Знайти які курси читає певний викладач.
def select_5(teacher_id):
    result = session.query(Subject.id, Subject.name) \
        .select_from(Subject).join(Teacher).filter(Teacher.id == teacher_id).all()
    return result

# 6. Знайти список студентів у певній групі.
def select_6(group_id):
    result = session.query(Student.id, Student.fullname) \
        .select_from(Student).filter(Student.group_id == group_id).all()
    return result

# 7. Знайти оцінки студентів у окремій групі з певного предмета.
def select_7(group_id, subject_id):
    result = session.query(Student.id, Student.fullname, Grade.grade) \
        .select_from(Grade).join(Student).filter(and_(Student.group_id == group_id, Grade.subject_id == subject_id)).all()
    return result

# 8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8(teacher_id):
    result = session.query(func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Subject).filter(Subject.teacher_id == teacher_id).scalar()
    return result

# 9. Знайти список курсів, які відвідує певний студент.
def select_9(student_id):
    result = session.query(Subject.id, Subject.name) \
        .select_from(Grade).join(Subject).filter(Grade.student_id == student_id).distinct().all()
    return result

# 10. Список курсів, які певному студенту читає певний викладач.
def select_10(student_id, teacher_id):
    result = session.query(Subject.id, Subject.name) \
        .select_from(Grade).join(Subject).filter(and_(Grade.student_id == student_id, Subject.teacher_id == teacher_id)).distinct().all()
    return result

if __name__ == '__main__':
    # Приклад використання функцій
    print(select_1())
    print(select_2(1))
    print(select_3(1))
    print(select_4())
    print(select_5(1))
    print(select_6(1))
    print(select_7(1, 1))
    print(select_8(1))
    print(select_9(1))
    print(select_10(1, 1))
