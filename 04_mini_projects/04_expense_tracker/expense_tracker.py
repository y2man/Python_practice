
expense_list= []

print("Welcome to the Expense Tracker!")


total= 0

try: 
    num_items= int(input("Please Enter the ammount of ithems you went to add : "))
    if num_items<0:
        exit("the ammount can't be negative please enter correct number")
    
    
    
    for x in range(num_items):
        item_name = str(input(f"Please enter the name of item {x+1}: "))
        checker = True
       
        
        while checker:
            
         try:
             item_ammount = float(input(f"Please enter the ammount of the item {x+1}: "))
             
             if item_ammount<0:
                 print("The ammount can't be neggative please enter correct number")
             else:
                 
                checker= False
         except ValueError:
            print("Please enter a valid number")
            
        expense_list.append((item_name,item_ammount))

except ValueError:
    print("Please enter a valid number")
    exit()
    

with open("expenses.txt", "w", encoding="utf-8") as file:
    for x in range(len(expense_list)):
        file.write(f"Item {x+1}: {expense_list[x][0]} - Amount: {expense_list[x][1]:.2f}\n")
        total = total + expense_list[x][1]

# --- FIX 2: Open in "r" mode to READ and print the file content ---
print("\n--- Saved Expenses from File ---")
try:
    with open("expenses.txt", "r", encoding="utf-8") as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    print("No expense file found yet.")
        
print(f"Total Expense: ${total:.2f}")

        


    
      

