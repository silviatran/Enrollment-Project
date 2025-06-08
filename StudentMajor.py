import mongoengine
from mongoengine import *
import datetime
from Major import Major


class StudentMajor(EmbeddedDocument):
    """
    Each time the Student adds a major, another instance of this class is added
    to the list of majors for that student. They will always be appended to the
    end of the list. Additionally, the declaration date of a major must not be past
    the current date.
    """

    studentMajorName = StringField(db_field='student_major_name', required=True)
    declarationDate = DateTimeField(db_field='declaration_date', required=True)

    def __init__(self, studentMajorName, declarationDate: datetime, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.studentMajorName = studentMajorName
        self.declarationDate = declarationDate

    def get_major(self):
        return self.studentMajorName


    def __str__(self):
        return f'Student Major: Major: {self.studentMajorName}, on date: {self.declarationDate}'


    def equals(self, other) -> bool:
        """
        Check if this student major is the same as the other student major instance.
        :param other: The StudentMajor that we are comparing to.
        :return: True if they are for the same product, false otherwise.
        """
        return self.studentMajorName == other.studentMajorName

