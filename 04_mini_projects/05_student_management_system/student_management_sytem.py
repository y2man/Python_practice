
student = {}


def name_exists(new_name):
    new_key = new_name.strip().lower()
    for existing_name in student:
        if existing_name.lower() == new_key:
            return True
    return False

# Add a student
def add_student():
    checker = True
    while checker:
        try:
            student_number = int(input("how many students the user wants to enter?: "))

            if student_number > 0:
                for x in range(student_number):
                    while True:
                        name = input(f"Enter student {x+1} name: ").strip()

                        if not name:
                            print("Name cannot be empty.")
                            continue

                        if name_exists(name):
                            print("this name already exists please enter another one")
                        else:
                            break

                    grade_checker = True
                    while grade_checker:
                        try:
                            grade = float(input(f"Enter student {x+1} grade: "))

                            if grade >= 0 and grade <= 100:
                                student[name] = grade
                                grade_checker = False
                            else:
                                print("enter a valid grade between 0 and 100")
                        except ValueError:
                            print("please enter a valid grade")

                checker = False

            else:
                print("The number of studnet's can't be less than 1")

        except ValueError:
            print("please enter valid number")



# Search for a student
def search_student():
    if not student:
        print("there is no student data saved")
        return

    search_name = input("Enter the name of the student to search for: ").strip()

    if not search_name:
        print("Name cannot be empty.")
        return

    for name, grade in student.items():
        if name.lower() == search_name.lower():
            print(f"Student {name} grade: {grade:.2f}")
            return

    print("Student not found.")



# Display all students
def display_students():
    if not student:
        print("there is no student data saved")
    else:
        for name, grade in student.items():
            print(f"Student: {name} | Grade: {grade:.2f}")



# Exit
def main():
    outer_checker = True

    while outer_checker:
        try:
            print("Please choose what you went to do:")
            print("1. Add a student")
            print("2. Search for a student")
            print("3. Display all students")
            print("4.Exit")
            choice= int(input("Your choice?: "))

            if choice==1:
                add_student()

            elif choice==2:
                search_student()

            elif choice==3:
                display_students()

            elif choice==4:
                print("You exited the system!")
                break

            else:
                print("please enter only numbers with in the choice range")

        except ValueError:
            print("Please enter valid number")


main()
            