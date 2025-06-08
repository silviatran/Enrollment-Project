from Menu import Menu
import logging
from Option import Option

menu_logging = Menu('debug', 'Please select the logging level from the following:', [
    Option("Debugging", "logging.DEBUG"),
    Option("Informational", "logging.INFO"),
    Option("Error", "logging.ERROR")
])

menu_main = Menu('main', 'Please select one of the following options:', [
    Option("Add new instance", "add()"),
    Option("Delete existing instance", "delete()"),
    Option("List existing instances", "list_members()"),
    Option("Select existing instance", "select()"),
    #Option("Update existing instance", "update()"),
    Option("Exit", "pass")
])

# options for adding a new instance
add_select = Menu('add select', 'Which type of object do you want to add?:', [
    Option("Students", "add_student()"),
    Option("Department", "add_department()"),
    Option("Major", "add_major()"),
    Option("Course", "add_course()"),
    Option("Section", "add_section()"),
    Option("Section to a selected student", "add_student_section()"),
    Option("Student to a selected section", "add_section_student()"),
    Option("Major to a selected student", "add_student_major()"),
    Option("Student to a selected major", "add_major_student()"),
    Option("Exit", "pass")
])

# options for deleting an existing instance
delete_select = Menu('delete select', 'Which type of object do you want to delete?:', [
    Option("Student", "delete_student()"),
    Option("Department", "delete_department()"),
    Option("Major", "delete_major()"),
    Option("Course", "delete_course()"),
    Option("Section", "delete_section()"),
    Option("Major from a selected student", "delete_student_major()"),
    Option("Student from a selected major", "delete_major_student()"),
    Option("Section from a selected student", "delete_student_section()"),
    Option("Student from a selected section", "delete_section_student()"),
    Option("Exit", "pass")
])

# options for listing the existing instances
list_select = Menu('list select', 'Which type of object do you want to list?:', [
    Option("Students", "list_students()"),
    Option("Departments", "list_departments()"),
    Option("Majors", "list_department_majors()"),
    Option("Department's courses", "list_department_courses()"),
    Option("Course's sections", "list_course_sections()"),
    Option("Student's majors", "list_student_majors()"),
    Option("Major's students", "list_major_students()"),
    Option("Student's sections", "list_student_sections()"),
    Option("Section's students", "list_section_students()"),
    Option("Exit", "pass")
])

# options for testing the select functions
select_select = Menu('select select', 'Which type of object do you want to select:', [
    Option("Student", "print(select_student())"),
    Option("Department", "print(select_department())"),
    Option("Major", "print(select_major())"),
    Option("Course", "print(select_course())"),
    Option("Section", "print(select_section())"),
    Option("Exit", "pass")
])

"""
#options for testing the update functions
update_select = Menu("update select", 'Which type of object do you want to update:', [
    Option("Order", "update_order()"),
    Option("Order Items", "update_order_item"),
    Option("Product", "update_product()"),
    Option("Exit", "pass")
])
"""
