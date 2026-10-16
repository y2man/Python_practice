num1 = float(input("Enter the numer of your choice: "))
print("choose the opration you went to perform")
print("1. Addition")
print("2. Subtraction")
print("3. Multiplication")
print("4. Division")

opr = int(input("Enter the number of your choice:"))

num2 = float(input("Enter the numer of your choice: "))

if opr==1:
    print("the sum of two numbers is : ", num1+num2)
elif opr==2:
    print("the differece of two numbers is : ",num1-num2)
elif opr==3:
    print("the product of two numbers is : ",num1*num2)
elif opr==4:
    print("the division of two numbers is : ",num1/num2)  
else : 
    print("you Entered the wrong choice please try again")          




