import os
from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    class_number = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class CognitiveGrade(Base):
    __tablename__ = "cognitive_grades"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=False)
    class_number = Column(Integer, nullable=False)
    homework = Column(Integer, default=0)
    participation = Column(Integer, default=0)
    performance_tasks = Column(Integer, default=0)
    tests = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class EducationalGrade(Base):
    __tablename__ = "educational_grades"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=False)
    class_number = Column(Integer, nullable=False)
    ratings = Column(JSON, default={})
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class BehavioralGrade(Base):
    __tablename__ = "behavioral_grades"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=False)
    class_number = Column(Integer, nullable=False)
    ratings = Column(JSON, default={})
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SelfAssessment(Base):
    __tablename__ = "self_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=False)
    class_number = Column(Integer, nullable=False)
    answers = Column(JSON, default={})
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        pass

def add_student(name: str, class_number: int):
    db = SessionLocal()
    try:
        existing = db.query(Student).filter(
            Student.name == name,
            Student.class_number == class_number
        ).first()
        if existing:
            return None
        student = Student(name=name, class_number=class_number)
        db.add(student)
        db.commit()
        db.refresh(student)
        return student
    finally:
        db.close()

def add_students_bulk(names: list, class_number: int):
    db = SessionLocal()
    try:
        added = []
        for name in names:
            existing = db.query(Student).filter(
                Student.name == name,
                Student.class_number == class_number
            ).first()
            if not existing:
                student = Student(name=name, class_number=class_number)
                db.add(student)
                added.append(name)
        db.commit()
        return added
    finally:
        db.close()

def get_students_by_class(class_number: int):
    db = SessionLocal()
    try:
        students = db.query(Student).filter(Student.class_number == class_number).all()
        return [s.name for s in students]
    finally:
        db.close()

def get_student_id(name: str, class_number: int):
    db = SessionLocal()
    try:
        student = db.query(Student).filter(
            Student.name == name,
            Student.class_number == class_number
        ).first()
        return student.id if student else None
    finally:
        db.close()

def delete_student(name: str, class_number: int):
    db = SessionLocal()
    try:
        student = db.query(Student).filter(
            Student.name == name,
            Student.class_number == class_number
        ).first()
        if student:
            db.query(CognitiveGrade).filter(CognitiveGrade.student_id == student.id).delete()
            db.query(EducationalGrade).filter(EducationalGrade.student_id == student.id).delete()
            db.query(BehavioralGrade).filter(BehavioralGrade.student_id == student.id).delete()
            db.query(SelfAssessment).filter(SelfAssessment.student_id == student.id).delete()
            db.delete(student)
            db.commit()
            return True
        return False
    finally:
        db.close()

def save_cognitive_grades(student_name: str, class_number: int, grades: dict):
    db = SessionLocal()
    try:
        student_id = get_student_id(student_name, class_number)
        if not student_id:
            return False
        
        existing = db.query(CognitiveGrade).filter(
            CognitiveGrade.student_id == student_id,
            CognitiveGrade.class_number == class_number
        ).first()
        
        if existing:
            existing.homework = grades.get('الواجبات', 0)
            existing.participation = grades.get('التفاعل والمشاركة', 0)
            existing.performance_tasks = grades.get('المهام الأدائية', 0)
            existing.tests = grades.get('درجة الاختبارات', 0)
            existing.updated_at = datetime.utcnow()
        else:
            grade = CognitiveGrade(
                student_id=student_id,
                class_number=class_number,
                homework=grades.get('الواجبات', 0),
                participation=grades.get('التفاعل والمشاركة', 0),
                performance_tasks=grades.get('المهام الأدائية', 0),
                tests=grades.get('درجة الاختبارات', 0)
            )
            db.add(grade)
        
        db.commit()
        return True
    finally:
        db.close()

def get_cognitive_grades(student_name: str, class_number: int):
    db = SessionLocal()
    try:
        student_id = get_student_id(student_name, class_number)
        if not student_id:
            return {}
        
        grade = db.query(CognitiveGrade).filter(
            CognitiveGrade.student_id == student_id,
            CognitiveGrade.class_number == class_number
        ).first()
        
        if grade:
            return {
                'الواجبات': grade.homework,
                'التفاعل والمشاركة': grade.participation,
                'المهام الأدائية': grade.performance_tasks,
                'درجة الاختبارات': grade.tests
            }
        return {}
    finally:
        db.close()

def save_educational_grades(student_name: str, class_number: int, ratings: dict):
    db = SessionLocal()
    try:
        student_id = get_student_id(student_name, class_number)
        if not student_id:
            return False
        
        existing = db.query(EducationalGrade).filter(
            EducationalGrade.student_id == student_id,
            EducationalGrade.class_number == class_number
        ).first()
        
        if existing:
            existing.ratings = ratings
            existing.updated_at = datetime.utcnow()
        else:
            grade = EducationalGrade(
                student_id=student_id,
                class_number=class_number,
                ratings=ratings
            )
            db.add(grade)
        
        db.commit()
        return True
    finally:
        db.close()

def get_educational_grades(student_name: str, class_number: int):
    db = SessionLocal()
    try:
        student_id = get_student_id(student_name, class_number)
        if not student_id:
            return {}
        
        grade = db.query(EducationalGrade).filter(
            EducationalGrade.student_id == student_id,
            EducationalGrade.class_number == class_number
        ).first()
        
        return grade.ratings if grade else {}
    finally:
        db.close()

def save_behavioral_grades(student_name: str, class_number: int, ratings: dict):
    db = SessionLocal()
    try:
        student_id = get_student_id(student_name, class_number)
        if not student_id:
            return False
        
        existing = db.query(BehavioralGrade).filter(
            BehavioralGrade.student_id == student_id,
            BehavioralGrade.class_number == class_number
        ).first()
        
        if existing:
            existing.ratings = ratings
            existing.updated_at = datetime.utcnow()
        else:
            grade = BehavioralGrade(
                student_id=student_id,
                class_number=class_number,
                ratings=ratings
            )
            db.add(grade)
        
        db.commit()
        return True
    finally:
        db.close()

def get_behavioral_grades(student_name: str, class_number: int):
    db = SessionLocal()
    try:
        student_id = get_student_id(student_name, class_number)
        if not student_id:
            return {}
        
        grade = db.query(BehavioralGrade).filter(
            BehavioralGrade.student_id == student_id,
            BehavioralGrade.class_number == class_number
        ).first()
        
        return grade.ratings if grade else {}
    finally:
        db.close()

def save_self_assessment(student_name: str, class_number: int, answers: dict):
    db = SessionLocal()
    try:
        student_id = get_student_id(student_name, class_number)
        if not student_id:
            return False
        
        existing = db.query(SelfAssessment).filter(
            SelfAssessment.student_id == student_id,
            SelfAssessment.class_number == class_number
        ).first()
        
        if existing:
            existing.answers = answers
            existing.updated_at = datetime.utcnow()
        else:
            assessment = SelfAssessment(
                student_id=student_id,
                class_number=class_number,
                answers=answers
            )
            db.add(assessment)
        
        db.commit()
        return True
    finally:
        db.close()

def get_self_assessment(student_name: str, class_number: int):
    db = SessionLocal()
    try:
        student_id = get_student_id(student_name, class_number)
        if not student_id:
            return {}
        
        assessment = db.query(SelfAssessment).filter(
            SelfAssessment.student_id == student_id,
            SelfAssessment.class_number == class_number
        ).first()
        
        return assessment.answers if assessment else {}
    finally:
        db.close()

def get_all_grades_for_class(class_number: int):
    db = SessionLocal()
    try:
        students = db.query(Student).filter(Student.class_number == class_number).all()
        result = []
        
        for student in students:
            row = {'name': student.name}
            
            cog = db.query(CognitiveGrade).filter(
                CognitiveGrade.student_id == student.id
            ).first()
            if cog:
                row['cognitive_total'] = cog.homework + cog.participation + cog.performance_tasks + cog.tests
            else:
                row['cognitive_total'] = None
            
            edu = db.query(EducationalGrade).filter(
                EducationalGrade.student_id == student.id
            ).first()
            row['educational'] = edu.ratings if edu else {}
            
            beh = db.query(BehavioralGrade).filter(
                BehavioralGrade.student_id == student.id
            ).first()
            row['behavioral'] = beh.ratings if beh else {}
            
            result.append(row)
        
        return result
    finally:
        db.close()
