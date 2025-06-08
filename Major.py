import mongoengine
from mongoengine import *
from Department import Department


class Major(Document):
    """A major belongs to one department, but a department can have 1 or more majors.
    A major can contain 0 or many students."""
    majorName = StringField(db_field='major_name', required=True)
    description = StringField(db_field='description', required=True)
    students = ListField(ReferenceField('Student'))

    department = ReferenceField(Department, required=True)

    meta = {'collection': 'majors',
            'indexes': [
                {'unique': True, 'fields': ['majorName'], 'name': 'majors_pk'}
            ]}

    def __init__(self, department, majorName, description, *args, **values):
        """
        Create a new instance of Major.
        :param name:  Individual name of a Major.
        :param description: Major's description.
        """

        super().__init__(*args, **values)
        if self.students is None:
            self.students = []
        self.department = department
        self.majorName = majorName
        self.description = description

    def get_students(self):
        return self.students

    def get_department(self):
        return self.department

    def get_name(self):
        return self.majorName

    def add_student(self, new_student):
        """

        Everytime the student adds a major, we add another instance of Student
        to the Major's list of students.
        """
        if self.students:
            for existing_student in self.students:
                if new_student.equals(existing_student):  # compares student names
                    print("The major already contains this student.")
                    return  # Major already has that student, don't add
            self.students.append(new_student)
        else: #first entry
            self.students = [new_student]

    def remove_student(self, student):
        """
        Removes a student from the major.
        :param major:    An instance of the Student class. If the student does not exist with the major
                        the call is ignored.
        :return:        None
        """
        for existing_student in self.students:
            if student.equals(existing_student):
                self.students.remove(existing_student)
                return

    def __str__(self):
        return f'Major Name: {self.majorName}, Description: {str(self.description)}'

    def equals(self, other) -> bool:
        return self.majorName == other.majorName
