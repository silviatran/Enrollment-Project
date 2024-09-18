# Enrollment-Project

## Project Overview
This Python application manages course enrollment in a university system using MongoDB and MongoEngine. The system is designed to enforce specific business rules regarding students, courses, departments, and enrollment while providing basic CRUD operations for each entity. The application ensures data integrity, preventing issues such as orphaned child documents and redundant data using MongoDB's unique constraints and Python error handling.

## Objectives
- Develop a Python application that performs basic CRUD operations on university courses, students, departments, and enrollments.
- Ensure that business rules such as uniqueness constraints, referential integrity, and data validation are implemented through MongoDB, MongoEngine, and Python code.
- Handle errors effectively using Python `try/except` blocks, and provide meaningful user feedback.
- Allow flexibility in adding, deleting, and listing course and enrollment data, while adhering to the constraints imposed by the data model.

## Key Features
- **CRUD Operations**: Users can add, delete, and list records for students, departments, courses, and sections.
- **Data Integrity**: Prevents orphaned child documents by enforcing business rules such as ensuring a department cannot be deleted while it still has associated courses or students.
- **Business Rule Enforcement**: Implements various business rules including course scheduling conflicts, uniqueness constraints, and valid ranges for attributes such as room number, course number, and semester.
- **Error Handling**: Uses MongoEngine and Python exceptions to manage data input errors, providing users with actionable feedback.
- **Flexible Data Design**: Supports the embedding and referencing of documents in MongoDB, making the system both flexible and efficient for different data structures.

## Business Rules Implemented
1. **Department**:
   - Unique abbreviation, chairperson, building, and office constraints.
   - Chairperson's name is limited to 80 characters, and building name is limited to 10 characters.

2. **Course**:
   - Each course belongs to exactly one department.
   - Courses are uniquely identified by department abbreviation and course number.
   - Course number must be between 100 and 700, and units must be between 1 and 5.

3. **Section**:
   - Each section must be unique by its course, section number, semester, and year.
   - Scheduling conflicts in the same building/room are avoided by comparing times.
   - Room numbers are constrained between 1 and 999.

4. **Student and Enrollment**:
   - Students can declare multiple majors and enroll in multiple sections.
   - A student cannot enroll in more than one section of the same course in the same semester.
   - Enrollment records are categorized as either pass/fail or letter grade.

## Requirements
- **Python 3.x**
- **MongoDB** (version 4.0 or higher)
- **MongoEngine** (ODM for MongoDB)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repository/university-enrollment-system.git
   cd university-enrollment-system
