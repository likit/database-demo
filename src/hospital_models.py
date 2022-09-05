import string
import random
from datetime import datetime

from faker import Faker
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Table, Float, func
from sqlalchemy.orm import declarative_base, relationship, backref, Session

Base = declarative_base()
engine = create_engine('sqlite:///hospital.db')


class TestLabOrderAssoc(Base):
    __tablename__ = 'test_lab_order_assoc'
    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    test_id = Column('test_id', ForeignKey('tests.id'))
    lab_order_id = Column('lab_order_id', ForeignKey('lab_orders.id'))


class Patient(Base):
    __tablename__ = 'patients'
    hn = Column('hn', Integer(), primary_key=True, autoincrement=True)
    firstname = Column('firstname', String(45), nullable=False)
    lastname = Column('lastname', String(45), nullable=False)
    dob = Column('dob', DateTime())
    gender = Column('gender', String(1))
    pid = Column('pid', String(13), unique=True, index=True)
    address = Column('address', String(255))
    province = Column('province', String(45))


class Visit(Base):
    __tablename__ = 'visits'
    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    datetime = Column('checkin', DateTime())
    patient_hn = Column('patient_hn', ForeignKey('patients.hn'))
    patient = relationship(Patient, backref=backref('visits', cascade='all, delete-orphan'))


class Department(Base):
    __tablename__ = 'departments'
    code = Column('code', String(4), primary_key=True)
    name = Column('name', String(255), nullable=False)


class Doctor(Base):
    __tablename__ = 'doctors'
    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    firstname = Column('firstname', String(45), nullable=False)
    lastname = Column('lastname', String(45), nullable=False)
    license = Column('license', String(45), unique=True, index=True)
    department_code = Column('department_code', ForeignKey('departments.code'))
    department = relationship(Department, backref=backref('doctors', cascade='all, delete-orphan'))


class Specimens(Base):
    __tablename__ = 'specimens'
    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    name = Column('specimens', String(45), nullable=False)
    site = Column('site', String(45))


class Test(Base):
    __tablename__ = 'tests'
    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    name = Column('name', String(45), nullable=False)
    price = Column('price', Float())
    ref = Column('ref', String(45))
    specimens_id = Column('specimens_id', ForeignKey('specimens.id'))
    specimens = relationship(Specimens)


class LabOrder(Base):
    __tablename__ = 'lab_orders'
    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    tests = relationship('Test', secondary='test_lab_order_assoc')
    visit_id = Column('visit_id', ForeignKey('visits.id'))
    doctor_id = Column('doctor_id', ForeignKey('doctors.id'))
    visit = relationship(Visit, backref=backref('lab_orders', cascade='all, delete-orphan'))
    doctor = relationship(Doctor)


if __name__ == '__main__':
    fake = Faker()
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        print('populating patient tables..')
        for n in range(300):
            pnt = Patient(
                firstname=fake.first_name(),
                lastname=fake.last_name(),
                dob=datetime.strptime(fake.date(), '%Y-%m-%d').date(),
                gender=random.choice(['f', 'm']),
                address=fake.street_address(),
                pid=''.join([random.choice(string.digits) for i in range(13)]),
                province=fake.city()
            )
            session.add(pnt)
        session.commit()

    dept_codes = [('OTH', 'Orthopedics'), ('ER', 'Emergency'), ('MED', 'Internal Medicine'), ('GYN', 'Gynecology')]

    with Session(engine) as session:
        print('populating department tables...')
        for code in dept_codes:
            dept = Department(code=code[0], name=code[1])
            session.add(dept)
        session.commit()

    with Session(engine) as session:
        print('populating doctor tables..')
        for n in range(30):
            pnt = Doctor(
                firstname=fake.first_name(),
                lastname=fake.last_name(),
                license=''.join([random.choice(string.digits) for i in range(10)]),
                department_code=random.choice(dept_codes)[0]
            )
            session.add(pnt)
        session.commit()

    with Session(engine) as session:
        print('populating specimens tables..')
        serum = Specimens(name='serum', site='blood')
        session.add(serum)
        session.commit()

    with Session(engine) as session:
        for test in ['Glucose', 'Triglyceride', 'Cholesterol', 'HDL', 'LDL', 'ALP']:
            session.add(Test(name=test, price=random.randint(100, 300), specimens=serum))
        session.commit()

    with Session(engine) as session:
        print('populating visit tables...')
        for n in range(100):
            patient = session.query(Patient).order_by(func.random()).first()
            visit = Visit(
                patient=patient,
                datetime=datetime.strptime(fake.date(), '%Y-%m-%d').date(),
            )
            session.add(visit)
            n = random.randint(0, 3)
            print('populating lab order table..')
            for i in range(n):
                t = random.randint(1, 4)
                doctor = session.query(Doctor).order_by(func.random()).first()
                tests = list(session.query(Test).order_by(func.random()).limit(t))
                order = LabOrder(
                    visit=visit,
                    doctor=doctor,
                    tests=tests
                )
                session.add(order)
        session.commit()
