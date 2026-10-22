from greetings import greet

message  = greet("Isaac")

print (message)
# when we ue fucntion with out return we return None and when we assign the call to 

#varible we will assign None to it bit it will call the real alue first and them if 
# we print that varible we will got None
class Calculator:
    def add(self, a, b):
        print(a + b)

calc = Calculator()

print("Result:", calc.add(3, 4))