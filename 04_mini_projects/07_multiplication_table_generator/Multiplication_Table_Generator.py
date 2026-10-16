checker = True

while checker:
    
    try:
        number = int(input("Enter a number to generate its multiplication table: "))
        
        for x in range(1,11):
            
            print(f" {number } X {x} = {number * x}")
            
        checker= False
        
    except ValueError:
        
        print("please enter valid number")    