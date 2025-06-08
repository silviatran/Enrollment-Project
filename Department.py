import mongoengine
from mongoengine import *
from Building import Building




class Department(Document):
    name = StringField(db_field='name', max_length= 70, required= True, unique=True)
    departmentAbbr = StringField(db_field='department_abbreviation', max_length=6, required=True)
    chairName = StringField(db_field='chair_name', max_length=80, required=True, unique=True)
    building = EnumField(Building, required=True, unique_with='office')
    office = StringField(db_field='office', required=True)
    description = StringField(db_field='department_description', required=True)

    courses = ListField(ReferenceField('Course')) #list of course objectIds
    majors = ListField(ReferenceField('Major'))


    meta = {'collection': 'departments',
        'indexes': [
            {'unique': True, 'fields': ['departmentAbbr'], 'name': 'departments_pk'}
        ]
    }

    def __init__(self, name, departmentAbbr, chairName, building: Building, office, description, *args, **values):
        super().__init__(*args, **values)
        if self.courses is None:
            self.courses = []
        if self.majors is None:
            self.majors = []
        self.name = name
        self.departmentAbbr = departmentAbbr
        self.chairName = chairName
        self.building = building
        self.office = office
        self.description = description

    def __str__(self):
        return f'Department name: {self.name}, Department Abbreviation: {self.departmentAbbr},' \
               f'Chair Name: {self.chairName}, Building: {self.building}, Office: {self.office}'


    def add_course(self, new_course):
        if self.courses:
            for existing_course in self.courses:
                if new_course.equals(existing_course):
                    print("The department already contains this course.")
                    return
            else:
                self.courses.append(new_course)
        else:  #first entry
             self.courses = [new_course]


    def remove_course(self, course):
        for existing_course in self.courses:
            if course.equals(existing_course):
                self.courses.remove(existing_course)
                return

    def add_major(self, new_major):
        if self.majors:
            for existing_major in self.majors:
                if new_major.equals(existing_major):
                    print("The department already contains this major.")
                    return
            else:
                self.majors.append(new_major)
        else:  #first entry
             self.majors = [new_major]

    def remove_major(self, major):
        for existing_major in self.majors:
            if major.equals(existing_major):
                self.majors.remove(existing_major)
                return


    def get_courses(self):
        return self.courses

    def get_majors(self):
        return self.majors