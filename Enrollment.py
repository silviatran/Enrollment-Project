import mongoengine
from mongoengine import *
from Student import Student
from Section import Section
from Semester import Semester
from Grade import Grade


class Enrollment(Document):
    student = ReferenceField(Student, required=True, reverse_delete_rule=mongoengine.DENY,
                             unique_with=['semester', 'sectionYear', 'departmentAbbvr', 'courseNumber'])

    section = ReferenceField(Section, required=True, reverse_delete_rule=mongoengine.DENY)
    departmentAbbvr = StringField(db_field='enr_department_abbr', required=True)
    courseNumber = IntField(db_field='enr_course_number', min_value=100, max_value=700, required=True)
    sectionNumber = IntField(db_field='enr_section_number', required=True)
    sectionYear = IntField(db_field='enr_section_year', required=True)
    semester = EnumField(Semester, required=True)
    #includes optional attributes from PassFail and LetterGrade


    meta = {'allow_inheritance': True,
            'collection': 'enrollments',
            'indexes': [
                {'unique': True, 'fields': ['student', 'departmentAbbvr', 'courseNumber', 'sectionNumber', 'sectionYear','semester'], 'name': 'enrollments_pk'}
            ]}


    def equals(self, other) -> bool:
        return (self.student == other.student) and (self.departmentAbbvr == other.departmentAbbvr) and (self.courseNumber == other.courseNumber)\
            and (self.sectionNumber == other.sectionNumber)\
            and (self.sectionYear == other.sectionYear) and (self.semester == other.semester)

    def __str__(self):
        return f'Enrollment: Student: {self.student.firstName, self.student.lastName}, Section: {self.departmentAbbvr, self.courseNumber, self.sectionNumber, self.sectionYear, self.semester}'

    def get_section(self):
        return self.section

    def get_student(self):
        return self.student

class PassFail(Enrollment):
    """Stored in the Enrollment collection. PassFail is not stored
    as its own collection."""
    applicationDate = DateTimeField(db_field='application_date')

class LetterGrade(Enrollment):
    """Stored in the Enrollment collection. LetterGrade is not
    stored as its own collection."""
    #minSatisfactory = StringField(db_field='min_satisfactory')
    minSatisfactory = EnumField(Grade, required=True)


