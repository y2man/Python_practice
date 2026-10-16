#Number Analyzer

negative_count=0
positive_count=0
odd_count = 0
even_count=0
zero_count=0


for count in range(1,6):
 checker=True
    
 while(checker):
    try:
  
        number = int(input(f"enter a number {count} : "))
                      
        if number > 0:
            positive_count+=1
        elif number<0:  
            negative_count+=1
        elif number==0:
            zero_count+=1        
        
        if number % 2==0:
                even_count+=1
        elif number % 2 !=0:
            odd_count+=1
        checker=False
          
    except ValueError:
        print("please enter a valid input")


print("--------Summery------")
print("positive numbers: ",positive_count)
print("negative numbers: ",negative_count)
print("zero numbers: ",zero_count)
print("even numbers: ",even_count)
print("odd numbers: ",odd_count)
        
    