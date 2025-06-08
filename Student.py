import mongoengine
from StudentMajor import StudentMajor
from mongoengine import *
from datetime import datetime


class Student(Document):
    """A Student can declare 0 or more majors.
    A student can be in 0 or more enrollments."""

    lastName= StringField(db_field='last_name', max_length=40, required=True)
    firstName = StringField(db_field='first_name', max_length=50, required=True)
    email = StringField(db_field='email', max_length=800, required=True, unique=True)
    studentMajors = EmbeddedDocumentListField(StudentMajor, db_field='student_majors')
    enrollments = ListField(ReferenceField('Enrollment'))

    meta = {'collection': 'students',
            'indexes': [
                {'unique': True, 'fields': ['firstName', 'lastName'], 'name': 'students_pk'}
            ]}

    def __init__(self, firstName, lastName, email, *args, **values):
        """
        Create a new instance of Student.
        :param studentID:   Individual code to student.
        :param lastName:   Student's last name.
        :param firstName:  Student's first name.
        :param email: Student's school email.
        """

        super().__init__(*args, **values)
        if self.enrollments is None:
            self.enrollments = []
        self.firstName = firstName
        self.lastName = lastName
        self.email = email

    def add_major(self, new_major: StudentMajor):
        """
        Everytime the student adds a major, we add another instance of StudentMajor
        to the Student's list of majors.
        """
        if self.studentMajors:
            for existing_major in self.studentMajors:
                if new_major.equals(existing_major): #compares major names
                    print("The student has already declared this major.")
                    return  # Student already has major, don't add it.
            if new_major.declarationDate > datetime.utcnow():
                raise ValueError('The price date cannot occur in the future.')
            else:
                self.studentMajors.append(new_major)
        else:  #first entry
            if new_major.declarationDate > datetime.utcnow():
                raise ValueError('The price date cannot occur in the future.')
            else:
                self.studentMajors = [new_major]

    def remove_major(self, major: StudentMajor):
        """
        Removes a major from the student.
        :param major:    An instance of the StudentMajor class. If this major does not exist with the student
                        the call is ignored.
        :return:        None
        """
        for existing_major in self.studentMajors:
            if major.equals(existing_major):
                self.studentMajors.remove(existing_major)
                return

    def get_majors(self):
        return self.studentMajors

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



    def __str__(self):
        return f'Student: First Name: {self.firstName}, Last Name: {str(self.lastName)}'

    def equals(self, other) -> bool:
        """
        Check if this student is the same as the other student instance.
        :param other: The Student that we are comparing to.
        :return: True if they are for the same product, false otherwise.
        """

        return (self.firstName == other.firstName) and (self.lastName == other.lastName)


