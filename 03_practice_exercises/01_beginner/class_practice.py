class Person:
    def __init__(self,name):
        self.name = name

class Student(Person):
    
    school = "AASTU"
    
    def __init__(self,name,grade=0):
        
        super().__init__(name)
        
        self._grade = 0 # Initialize the private attribute _grade to 0
       
        self.grade = grade
        
        
    def display_info(self):
        
        print(f"Hi {self.name} Your grade is {self.grade} ")
        
    @property
    def grade(self):
        return self._grade
    @grade.setter

    def grade(self,grade):
        try: 
            if grade>=0 and grade<=100:
                
            
                    self._grade = grade
            else:
                print("The grade Can't be less than 0 or greater than 100")
        except TypeError:
            print("Invalid grade value. Please enter a number between 0 and 100.")

    def get_status(self):
        
        if self.grade>= 50:
            return "You Passed!"
        else:
            return "You Failed!"
        
        
        
student1 = Student("Sara", 80)
print(student1.grade)  # 80

student1.grade = 90
print(student1.grade)  # 90

student1.grade = 150
print(student1.grade)  # Should remain 90



