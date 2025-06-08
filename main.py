from ConstraintUtilities import select_general, unique_general, prompt_for_date
from Utilities import Utilities
from CommandLogger import CommandLogger, log
from pymongo import monitoring
from decimal import *

from Student import Student
from StudentMajor import StudentMajor
from Major import Major
from Department import Department
from Course import Course
from Section import Section
from Enrollment import Enrollment, PassFail, LetterGrade

from Menu import Menu
from Option import Option
from menu_definitions import menu_main, add_select, list_select, select_select, delete_select #update_select


def menu_loop(menu: Menu):
    """Little helper routine to just keep cycling in a menu until the user signals that they
    want to exit.
    :param  menu:   The menu that the user will see."""
    action: str = ''
    while action != menu.last_action():
        action = menu.menu_prompt()
        print('next action: ', action)
        exec(action)


def add():
    menu_loop(add_select)


def list_members():
    menu_loop(list_select)


def select():
    menu_loop(select_select)


def delete():
    menu_loop(delete_select)


def update():
    menu_loop(update_select)

def prompt_for_enum(prompt: str, cls, attribute_name: str):
    """
    MongoEngine attributes can be regulated with an enum.  If they are, the definition of
    that attribute will carry the list of choices allowed by the enum (as well as the enum
    class itself) that we can use to prompt the user for one of the valid values.  This
    represents the 'don't let bad data happen in the first place' strategy rather than
    wait for an exception from the database.
    :param prompt:          A text string telling the user what they are being prompted for.
    :param cls:             The class (not just the name) of the MongoEngine class that the
                            enumerated attribute belongs to.
    :param attribute_name:  The NAME of the attribute that you want a value for.
    :return:                The enum class member that the user selected.
    """
    attr = getattr(cls, attribute_name)  # Get the enumerated attribute.
    if type(attr).__name__ == 'EnumField':  # Make sure that it is an enumeration.
        enum_values = []
        for choice in attr.choices:  # Build a menu option for each of the enum instances.
            enum_values.append(Option(choice.value, choice))
        # Build an "on the fly" menu and prompt the user for which option they want.
        return Menu('Enum Menu', prompt, enum_values).menu_prompt()
    else:
        raise ValueError(f'This attribute is not an enum: {attribute_name}')



def check_student_unique(new_student):
    for student in Student.objects():
        if student.equals(new_student):
            return False
    return True

def select_student():
    return select_general(Student)

def select_major():
    dept = select_department()
    majors = dept.get_majors()
    menu_items: [Option] = []

    for major in majors:
        menu_items.append(Option(major.__str__(), major))

    major_choice = Menu('Majors Menu',
                         'Choose Major', menu_items).menu_prompt()
    return major_choice


def select_department():
    return select_general(Department)

def select_course():
    dept = select_department()
    courses = dept.get_courses()
    menu_items: [Option] = []

    for course in courses:
        menu_items.append(Option(course.__str__(), course))

    course_choice = Menu('Courses Menu',
                          'Choose Course', menu_items).menu_prompt()
    return course_choice


def select_section():
    course = select_course()
    sections = course.get_sections()
    menu_items: [Option] = []

    for sec in sections:
        menu_items.append(Option(sec.__str__(), sec))

    section_choice = Menu('Sections Menu',
                       'Choose Section', menu_items).menu_prompt()
    return section_choice

def add_student():
    """
            Create a new Student instance.
            :return: None
            """
    success: bool = False
    new_student = None
    while not success:
        firstn = input("First name-->")
        lastn = input("Last name-->")
        email = input("email-->")


        new_student = Student(firstn, lastn, email)
        #violated_constraints = unique_general(new_student)
        unique = check_student_unique(new_student)
        if unique: #continue to save
            try:
                new_student.save()
                success = True
            except Exception as e:
                print('Errors storing the new student:')
                text = Utilities.print_exception(e)
                print(text)

        else:
            print("This student is not unique. Please try again.")



def add_major():
    """
    Create a new Major instance.
    :return: None
    """
    success: bool = False
    new_major = None
    while not success:
        dept = select_department()
        name = input("Major name-->")
        descr = input("Major description-->")

        new_major = Major(dept, name, descr)
        violated_constraints = unique_general(new_major)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            try:
                new_major.save()
                dept.add_major(new_major)
                dept.save()
                success = True
            except Exception as e:
                print('Errors storing the new student:')
                text = Utilities.print_exception(e)
                print(text)

def add_department():
    success: bool = False
    new_dept = None
    while not success:
        name = input("Department Name-->")
        abbr = input("Department Abbreviation-->")
        chairName = input("Chair Name-->")
        building = prompt_for_enum('Select the building:', Department, 'building')
        office = input("Office-->")
        descr = input("Description-->")

        new_dept = Department(name, abbr, chairName, building, office, descr)
        violated_constraints = unique_general(new_dept)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            try:
                new_dept.save()
                success = True
            except Exception as e:
                print('Errors storing the new student:')
                text = Utilities.print_exception(e)
                print(text)

def add_course():
    success: bool = False
    new_course = None
    while not success:
        department = select_department()
        courseNumber = int(input("Course Number-->"))
        courseName = input("Course Name-->")
        descr = input("Description-->")
        units = int(input("Units-->"))


        new_course = Course(department, courseNumber,courseName, descr, units, departmentAbbreviation=department.departmentAbbr)
        violated_constraints = unique_general(new_course)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            try:
                new_course.save()
                department.add_course(new_course)
                department.save()
                success = True
            except Exception as e:
                print('Errors storing the new student:')
                text = Utilities.print_exception(e)
                print(text)


def add_section():
    """
    Create a new Section instance.
    :return: None
    """
    success: bool = False
    new_section = None
    while not success:
        course = select_course()
        sectionNumber = input("Section number-->")
        sectionYear = int(input("Section year-->"))
        schedule = prompt_for_enum('Select the schedule:', Section, 'schedule')
        semester = prompt_for_enum('Select the semester:', Section, 'semester')
        building = prompt_for_enum('Select the building:', Section, 'building')
        room = int(input("Room-->"))
        startTime = prompt_for_date("Enter start time: ")
        instructor = input("Instructor-->")

        new_section = Section(course, sectionNumber, sectionYear, schedule, semester, room, building, startTime, instructor,
                              departmentAbbv=course.departmentAbbreviation, courseNumber=course.courseNumber)

        violated_constraints = unique_general(new_section)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            try:
                new_section.save()
                course.add_section(new_section) #pass in Section instance
                course.save()
                success = True
            except Exception as e:
                print('Errors storing the new student:')
                text = Utilities.print_exception(e)
                print(text)


def add_student_major():

    success: bool = False
    new_student_major: StudentMajor
    student: Student
    while not success:
        student = select_student()

        major = select_major()
        date = prompt_for_date("Enter declaration date for this major: ")
        new_student_major = StudentMajor(major.get_name(), date)

        try:
            student.add_major(new_student_major)
            major.add_student(student)
            student.save()
            major.save()
            success = True
        except Exception as e:
            print('Exception trying to add the new item:')
            print(Utilities.print_exception(e))

def add_major_student():

    success: bool = False
    new_student_major: StudentMajor
    major: Major
    while not success:
        major = select_major()

        student = select_student()
        date = prompt_for_date("Enter declaration date for this major: ")
        new_student_major = StudentMajor(major.get_name(), date)

        try:
            #new_student_major.save()
            student.add_major(new_student_major)
            major.add_student(student)
            student.save()
            major.save()
            success = True
        except Exception as e:
            print('Exception trying to add the new item:')
            print(Utilities.print_exception(e))


def add_student_section(): #enrollment
    student = select_general(Student)
    section = select_general(Section)

    choice = input("Would you like to create a PassFail or LetterGrade enrollment?\n.1 PassFail \n2.LetterGrade\n")
    if choice == "1":  #PassFail
        app_date = prompt_for_date('Date and time of application: ')
        new_enrollment = PassFail(student=student, departmentAbbvr=section.departmentAbbv, section=section, applicationDate=app_date,
                                  courseNumber=section.courseNumber, sectionNumber=section.sectionNumber,
                                  semester=section.semester, sectionYear=section.sectionYear
                                  )
    else:     #Lettergrade
        #min = input("Please enter a minimum satisfactory grade: ")
        min = prompt_for_enum('Select Minimum Satisfactory Grade:', LetterGrade, 'minSatisfactory')
        new_enrollment = LetterGrade(student=student, departmentAbbvr=section.departmentAbbv, section=section, minSatisfactory=min,
                                     courseNumber=section.courseNumber, sectionNumber=section.sectionNumber,
                                     semester=section.semester, sectionYear=section.sectionYear
                                     )



    try:
        new_enrollment.save()
        student.add_enrollment(new_enrollment)
        section.add_enrollment(new_enrollment)
        student.save()
        section.save()
    except Exception as e:
        print('Errors storing the new enrollment:')
        text = Utilities.print_exception(e)
        print(text)

def add_section_student(): #enrollment
    section = select_general(Section)
    student = select_general(Student)

    choice = input("Would you like to create a PassFail or LetterGrade enrollment?\n.1 PassFail \n2.LetterGrade")
    if choice == "1":  #PassFail
        app_date = prompt_for_date('Date and time of application: ')
        new_enrollment = PassFail(student=student, departmentAbbvr=section.departmentAbbv, section=section, applicationDate=app_date,
                                  courseNumber=section.courseNumber, sectionNumber=section.sectionNumber,
                                  semester=section.semester, sectionYear=section.sectionYear)
    else:     #Lettergrade
        #min = input("Please enter a minimum satisfactory grade: ")
        min = prompt_for_enum('Select Minimum Satisfactory Grade:', LetterGrade, 'minSatisfactory')
        new_enrollment = LetterGrade(student=student, departmentAbbvr=section.departmentAbbv, section=section, minSatisfactory=min,\
                                     courseNumber=section.courseNumber, sectionNumber=section.sectionNumber,\
                                     semester=section.semester, sectionYear=section.sectionYear)



    try:
        new_enrollment.save()
        student.add_enrollment(new_enrollment)
        section.add_enrollment(new_enrollment)
        student.save()
        section.save()
    except Exception as e:
        print('Errors storing the new enrollment:')
        text = Utilities.print_exception(e)
        print(text)



def list_students():
    students = Student.objects()
    if not students:
        print("No students found in the database.")
    else:
        for student in students:
            print(student)

def list_department_majors():
    department = select_department()
    majors = department.get_majors()
    if not majors:
        print(f"No majors found in department: {department}")
    else:
        for major in majors:
            print(major)

def list_student_majors():
    student = select_student()
    majors = student.get_majors()
    if not majors:
        print(f"{student} has no declared majors.")
    else:
        for major in majors:
            print(major)

def list_major_students():
    major = select_major()
    students = major.get_students()
    if not students:
        print(f"No students declared this major: {major}")
    else:
        for student in students:
            print(student)

def list_departments():
    departments = Department.objects()
    if not departments:
        print("No departments found.")
    else:
        for dept in departments:
            print(dept)

def list_department_courses():
    dept = select_department()
    courses = dept.get_courses()
    if not courses:
        print(f"No courses found in department: {dept}")
    else:
        for course in courses:
            print(course)

def list_course_sections():
    course = select_course()
    sections = course.get_sections()
    if not sections:
        print(f"No sections found for course: {course}")
    else:
        for section in sections:
            print(section)

def list_student_sections():
    student = select_student()
    enrollments = student.get_enrollments()
    if not enrollments:
        print(f"{student} is not enrolled in any sections.")
    else:
        print(f"{student} is enrolled in the following sections:")
        for enrollment in enrollments:
            print(enrollment.section)

def list_section_students():
    section = select_section()
    enrollments = section.get_enrollments()
    if not enrollments:
        print(f"No students enrolled in section: {section}")
    else:
        print(f"{section} has the following enrolled students:")
        for enrollment in enrollments:
            print(enrollment.student)



def delete_student():
    """
    Delete an existing student from the database.
    :return: None
    """
    student = select_student() #checks existence
    majors = student.get_majors() #returns StudentMajors
    sections = student.get_enrollments()
    if majors:
        print("Student contains the following majors still: ")
        for major in majors:
            print(major)
        print("Remove the majors from the student first.")
    if sections:
        print("Student contains the following sections still: ")
        for section in sections:
            print(section)
        print("This student still has sections. Remove the sections from the student first.")
    if (len(majors) == 0) and (len(sections) == 0): #student has no majors or sections associated
        student.delete()



def delete_major():
    """
    Delete an existing major from the database.
    :return: None
    """
    major = select_major()
    students = major.get_students()
    department = major.get_department()
    if students:
        print("The major contains the following students still. Remove the students from the major first.")
        for student in students:
            print(student)
    else: #major contains no students
        department.remove_major(major)
        department.save()
        major.delete()

def delete_department():
    dept = select_department()
    courses = dept.get_courses()
    majors = dept.get_majors()
    if courses:
        print("This department still contains courses. Cannot delete department")
    elif majors:
        print("This department still has majors. Cannot delete department.")
    else:
        dept.delete()


def delete_course():
    course = select_course()
    sections = course.get_sections()
    if sections:
        print("This course still contains sections. Cannot delete course.")
    else:
        dept = course.get_department()
        dept.remove_course(course)
        dept.save()
        course.delete()

def delete_section():
    section = select_section()
    enrollments = section.get_enrollments()
    if enrollments:
        print("Section still contains enrolled students. Cannot delete section.")
    else: #Section has no students
        course = section.get_course()
        course.remove_section(section)
        course.save()
        section.delete()

def delete_student_section(): #enrollment
    """
    Delete an existing section from a selected student from the database.
    :return: None
    """

    student = select_student()
    enrollments = student.get_enrollments()
    if len(enrollments) == 0:
        print("Student contains no sections to delete.")
        return
    menu_items: [Option] = []

    for enr in enrollments:
        menu_items.append(Option(enr.__str__(), enr))

    enr_removal = Menu('Sections Menu',
                        'Choose which enrollment to remove', menu_items).menu_prompt()
    section = enr_removal.get_section()
    student.remove_enrollment(enr_removal)
    student.save()
    section.remove_enrollment(enr_removal)
    section.save()
    enr_removal.delete()

def delete_section_student():
    """
    Delete an existing student from a selected section from the database.
    :return: None
    """

    section = select_section()
    enrollments = section.get_enrollments()
    if len(enrollments) == 0:
        print("Section contains no students to delete.")
        return
    menu_items: [Option] = []

    for enr in enrollments:
        menu_items.append(Option(enr.__str__(), enr))
    enr_removal = Menu('Students Menu',
                       'Choose which enrollment to remove', menu_items).menu_prompt()
    student = enr_removal.get_student()
    section.remove_enrollment(enr_removal)
    section.save()
    student.remove_enrollment(enr_removal)
    student.save()
    enr_removal.delete()

def delete_student_major():
    student = select_student()
    majors = student.get_majors() #returns StudentMajors
    if len(majors) == 0:
        print("Student has no majors.")
    else:
        menu_items: [Option] = []
        for major in majors:
            menu_items.append(Option(major.__str__(), major))

        major_removal = Menu('Majors Menu',
                           'Choose which major to remove', menu_items).menu_prompt()


        student.remove_major(major_removal) #pass in StudentMajor
        student.save()

        #find major instance as opposed to StudentMajor
        delete_major = major_removal.get_major() #StudentMajor's getmajor() method returns name of major
        delete_major = Major.objects(majorName=delete_major).first() #returns major object
        delete_major.remove_student(student)
        delete_major.save()


def delete_major_student():
    major = select_major()
    students = major.get_students()
    if len(students) == 0:
        print("Major has no students.")
    else:
        menu_items: [Option] = []
        for student in students:
            menu_items.append(Option(student.__str__(), student))

        student_removal = Menu('Students Menu',
                             'Choose which student to remove', menu_items).menu_prompt()

        major.remove_student(student_removal)
        major.save()
        #find studentmajor to delete


        stud_majors = student_removal.get_majors() #returns all student's StudentMajors
        remove_stu_major: StudentMajor #specific StudentMajor embedding to delete
        for stud_major in stud_majors:
            if stud_major.get_major() == major.get_name():
                remove_stu_major = stud_major

        student.remove_major(remove_stu_major)  # pass in StudentMajor
        student.save()


if __name__ == '__main__':
    print('Starting in main.')
    monitoring.register(CommandLogger())
    db = Utilities.startup()
    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)
    log.info('All done for now.')
