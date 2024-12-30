import random
from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

from conf.db import session  # Імпортуємо сесію з db.py
from conf.models import Group, Teacher, Subject, Student, Grade  # Імпортуємо моделі
import logging

# Ініціалізація Faker
fake = Faker()

def seed_groups():
    try:
        groups = [
            Group(name=fake.word()) for _ in range(3)  # 3 групи
        ]
        session.add_all(groups)
        session.commit()
        print("Групи успішно додано.")
    except SQLAlchemyError as e:
        logging.error(f"Помилка при додаванні груп: {e}")
        session.rollback()

def seed_teachers():
    try:
        teachers = [
            Teacher(fullname=fake.name()) for _ in range(3)  # 3 викладачі
        ]
        session.add_all(teachers)
        session.commit()
        print("Викладачі успішно додані.")
    except SQLAlchemyError as e:
        logging.error(f"Помилка при додаванні викладачів: {e}")
        session.rollback()

def seed_subjects():
    try:
        teachers = session.query(Teacher).all()
        subjects = []
        for teacher in teachers:
            for _ in range(2):  # 2 предмети на викладача, всього 6-8
                subjects.append(Subject(name=fake.word(), teacher_id=teacher.id))
        session.add_all(subjects)
        session.commit()
        print("Предмети успішно додані.")
    except SQLAlchemyError as e:
        logging.error(f"Помилка при додаванні предметів: {e}")
        session.rollback()

def seed_students():
    try:
        groups = session.query(Group).all()
        students = []
        for group in groups:
            for _ in range(10):  # 10 студентів на групу, всього 30
                students.append(Student(fullname=fake.name(), group_id=group.id))
        session.add_all(students)
        session.commit()
        print("Студенти успішно додані.")
    except SQLAlchemyError as e:
        logging.error(f"Помилка при додаванні студентів: {e}")
        session.rollback()

def seed_grades():
    try:
        students = session.query(Student).all()
        subjects = session.query(Subject).all()
        grades = []
        for student in students:
            for subject in subjects:
                for _ in range(3):  # 3 оцінки на предмет, до 20 оцінок на студента
                    grades.append(
                        Grade(
                            student_id=student.id,
                            subject_id=subject.id,
                            grade=random.randint(1, 100),
                            grade_date=fake.date_this_decade(),
                        )
                    )
        session.add_all(grades)
        session.commit()
        print("Оцінки успішно додані.")
    except SQLAlchemyError as e:
        logging.error(f"Помилка при додаванні оцінок: {e}")
        session.rollback()

if __name__ == "__main__":
    seed_groups()
    seed_teachers()
    seed_subjects()
    seed_students()
    seed_grades()
