import mongoengine
from mongoengine import *
from Department import Department



class Course(Document):
    department = ReferenceField(Department, required=True, reverse_delete_rule=mongoengine.DENY)
    #departmentAbbr = StringField(db_field='department_abbreviation', required=True) #maybe?
    departmentAbbreviation = StringField(db_field='course_department_abbr', required=True, unique_with='courseNumber')
    courseNumber = IntField(db_field='course_number', min_value=100, max_value=700, required=True)
    courseName = StringField(db_field='course_name', required=True, unique_with='departmentAbbreviation')
    description = StringField(db_field='course_description', required=True)
    units = IntField(db_field='units', required=True, min_value=1, max_value=5)

    sections = ListField(ReferenceField('Section'))


    meta = {'collection': 'courses',
            'indexes': [
                {'unique': True, 'fields': ['departmentAbbreviation', 'courseNumber'], 'name': 'courses_pk'}
            ]
            }

    def __init__(self, department, courseNumber, courseName, description, units, *args, **values): #pass in Department object
        super().__init__(*args, **values)
        if self.sections is None:
            self.sections = []
        self.department = department
        self.courseNumber = courseNumber
        self.courseName = courseName
        self.description = description
        self.units = units

    def __str__(self):
        return f'Course Number: {self.courseNumber}, Course Name: {self.courseName}'


    def add_section(self, new_section):
        if len(self.sections) != 0:
            for existing_section in self.sections:
                if new_section.equals(existing_section):
                    return
                else:
                    self.sections.append(new_section)
        else:  #first entry
             self.sections = [new_section]


    def remove_section(self, section):
        for existing_section in self.sections:
            if section.equals(existing_section):
                self.sections.remove(existing_section)
                return


    def get_sections(self):
        return self.sections

    def get_department(self):
        return self.department

    def equals(self, other) -> bool:
        return (self.courseNumber == other.courseNumber)  and (self.department.departmentAbbr == other.department.departmentAbbr)

