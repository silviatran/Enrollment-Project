import mongoengine

from mongoengine import *
import Schedule
from Schedule import Schedule
from Semester import Semester
from Building import Building
from Course import Course


class Section(Document):
    course = ReferenceField(Course, required=True, reverse_delete_rule=mongoengine.DENY)
    departmentAbbv = StringField(db_field='section_department_abbr', required=True)
    courseNumber = IntField(db_field='sec_course_number', min_value=100, max_value=700, required=True)

    sectionNumber = IntField(db_field='section_number', required=True)
    sectionYear = IntField(db_field='section_year', required=True)
    schedule = EnumField(Schedule, required=True)
    semester = EnumField(Semester, required=True, unique_with=['sectionYear', 'building', 'room', 'schedule', 'startTime'])
    room = IntField(db_field='room', min_value=1, max_value=1000, required=True)
    building = EnumField(Building, required=True)
    startTime = DateTimeField(db_field='start_time', required=True)  # needs hr constraint
    instructor = StringField(db_field='instructor', required=True, unique_with=['semester', 'sectionYear', 'schedule', 'startTime'])

    enrollments = ListField(ReferenceField('Enrollment'))


    meta = {'collection': 'sections',
            'indexes': [
                {'unique': True, 'fields': ['departmentAbbv', 'courseNumber', 'sectionNumber', 'semester', 'sectionYear'], 'name': 'sections_pk'}
            ]}

    def __init__(self, course: Course, sectionNumber, sectionYear, schedule: Schedule, semester: Semester, room, building: Building, startTime, instructor, *args, **values):
        super().__init__(*args, **values)
        if self.enrollments is None:
            self.enrollments = []
        self.course = course
        self.sectionNumber = sectionNumber
        self.sectionYear = sectionYear
        self.schedule = schedule
        self.semester = semester
        self.room = room
        self.building = building
        self.startTime = startTime
        self.instructor = instructor



    def __str__(self):
        return f'Course: {self.departmentAbbv, self.courseNumber}, Section Number: {self.sectionNumber}, Section Year: {self.sectionYear}, Schedule: {self.schedule},' \
               f'Semester: {self.semester}, Room: {self.room}, Building: {self.building},' \
               f'Start Time: {self.startTime}, Instructor: {self.instructor}'






    def add_enrollment(self, new_enrollment):
        for existing_enrollment in self.enrollments:
            if new_enrollment.equals(existing_enrollment):
                print("The student already has this section.")
                return  # Student already has major, don't add it.
        self.enrollments.append(new_enrollment)

    def remove_enrollment(self, enrollment):
        for existing_enrollment in self.enrollments:
            if enrollment.equals(existing_enrollment):
                self.enrollments.remove(existing_enrollment)
                return

    def get_enrollments(self):
        return self.enrollments

    def get_course(self):
        return self.course

    def equals(self, other) -> bool:
        return (self.course == other.course) and (self.sectionNumber == other.sectionNumber) \
            and (self.sectionYear == other.sectionYear) and (self.semester == other.semester)