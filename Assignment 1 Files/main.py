import pickle
import sys
import os
import re


# Class to store user data
class Person:
    last = ''
    first = ''
    mi = ''
    ID = ''
    phone = ''

    # Person Constructor
    def __init__(self, last, first, mi, ID, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.ID = ID
        self.phone = phone

    # Prints Person information
    def display(self):
        print('Employee id:', self.ID)
        print('\t' + self.first, self.mi, self.last)
        print('\t' + self.phone)
        print()


'''
# Reads file from filepath
# Input: filepath
# Return: file data as text
'''
def read_file(filepath):
    with open(os.path.join(os.getcwd(), filepath), 'r') as f:
        text_in = f.read()
    return text_in


'''
# Breaks down input file, and stores into employee Person list (data is NOT cleaned)
# Input: file data
# Return: list of unclean employee Person objects
'''
def process_data(data):
    processed_employees = []
    # Split text file on newlines. This will create a list where each element holds a particular person's information
    split_data = data.split('\n')
    # Remove the header line
    split_data.pop(0)

    # Loop through each person's data and store their information in a new person
    for line in split_data:
        # Split on commas, store each item into corresponding Person attribute
        temp_p = line.split(',')
        new_person = Person(temp_p[0], temp_p[1], temp_p[2], temp_p[3], temp_p[4])
        # Add new person to list of employees
        processed_employees.append(new_person)

    return processed_employees


'''
# Takes list of uncleaned employee Person objects and cleans the data by prompting the user to input corrected data
# Input: List of uncleaned employee Person objects
# Return: List of cleaned employee Person objects
'''
def clean_data(processed_employees):
    # Loop through list of processed employees; clean each one
    for emp in processed_employees:
        # Capitalize first and last names
        emp.first = emp.first.capitalize()
        emp.last = emp.last.capitalize()

        # Capitalize middle initial
        emp.mi = emp.mi.capitalize()
        # Replace middle initial with 'X' if it is missing
        if not emp.mi:
            emp.mi = 'X'

        # Clean employee ID with regex
        pattern = '[A-Z]{2}\d{4}' # Regex pattern for matching ID (2 capital letters followed by 4 digits)
        while not re.fullmatch(pattern, emp.ID):
            print('ID invalid:', emp.ID)
            print('ID is two letters followed by 4 digits')
            emp.ID = input('Please enter a valid id: ')

        pattern = '\d{3}-\d{3}-\d{4}'  # Regex pattern for matching phone number (3 digits, 3 digits, 4 digits, hypen-separated)
        while not re.fullmatch(pattern, emp.phone):
            print('Phone', emp.phone, "is invalid")
            print('Enter phone number in form 123-456-7890')
            emp.phone = input('Enter phone number: ')

    return processed_employees


'''
# Converts a list of employees into a dict where the key is the employees ID and the value is the Person object
# If there are any repeated employee IDs, they are removed and an error message is displayed
# Input: List of employee Person objects
# Return: Dict of employee Person objects
'''
def employee_list_to_dict(employees):
    employee_dict = {}

    # Loop through employees, add each to dict
    for emp in employees:
        # Check if employee ID already exists. If so, print error message and move on
        if emp.ID in employee_dict:
            print('Error. Duplicate ID. Employee ' + emp.first, emp.mi, emp.last, "not added.")
        # If employee ID does not exist in dict, add to dict
        else:
            employee_dict[emp.ID] = emp

    return employee_dict


def main():
    # If no filepath is entered, print error and quit
    if len(sys.argv) < 2:
        print('Error. Please enter a filename as a system arg.')
        quit()

    # Read in data from given filepath, store in 'data' variable
    fp = sys.argv[1]
    data = read_file(fp)

    # Process the data text file into list of employee Person objects (uncleaned)
    processed_employees = process_data(data)
    # Clean each employee Person object by prompting the user to enter corrected information
    cleaned_data = clean_data(processed_employees)

    # Convert list of employees to dict of employees
    employee_dict = employee_list_to_dict(cleaned_data)

    # Save dictionary as a pickle file
    with open('employee_dict_pickle', 'wb') as handle:
        pickle.dump(employee_dict, handle)

    # Unpack the pickle file dict
    with open('employee_dict_pickle', 'rb') as handle:
        new_employee_dict = pickle.load(handle)

    # Print employee information to ensure pickle was unpickled correctly
    for emp_ID, emp in (new_employee_dict.items()):
        emp.display()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
