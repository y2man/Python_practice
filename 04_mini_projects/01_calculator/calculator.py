
checker = True

while checker: 
    
    try:
        number1 = float(input("Enter a number 1: "))
        number2= float(input("Enter a number 2: "))
        
        print("Choose the opration.")
        print ("1. Addition")
        print ("2. Substraction")
        print ("3. Multiplication")
        print ("4. Division")
        print("5. Exponentiation")
        print("6. Modulus")
        opration = int(input("choose the opration you went to perform: "))
        
        if opration ==1:
         print(f"{number1} + {number2} = {number1 + number2}")
        elif opration ==2:
         print(f"{number1} - {number2} = {number1 - number2}")
        elif opration ==3:
         print(f"{number1} * {number2} = {number1 * number2}")
        elif opration ==4:
            if number2==0:
                print("division by zero is not allowed")
                continue
            else:
                print(f"{number1} / {number2} = {number1 / number2}")
        elif opration ==5:
         print(f"{number1} ** {number2} = {number1 ** number2}")
        elif opration ==6:
            if number2==0:
                print("division by zero is not allowed")
                continue
            else:
                   print(f"{number1} % {number2} = {number1 % number2}")
        else: 
            print("Please enter only number between 1-6")
        choice = str(input("Whould you like to perfor another opration ?(y/n)"))
        if choice.lower() != 'y':
            checker = False
    except ValueError:
        print("Please enter a valid number")
        