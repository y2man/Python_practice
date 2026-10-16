#print("Python quiz!")

# correct_ansewrs= 0;

# question1 = str(input("Question 1. how many loop types are in python?: "))

# if question1=="3" or question1.lower()=="three":
#     print("correct!")
#     correct_ansewrs += 1
# else:
#     print("Incorrect!")

# question2 = str(input("Question 2. what is the method name called to change the string lower?: "))

# if question2.lower()=="lower":
#     print("correct!")
#     correct_ansewrs +=1
# else:
#     print("Incorrect!")

# question3 = str(input("Question 3. True or False. is argument and parameter same?: "))

# if question3.lower()=="false":
#     print("correct!")
#     correct_ansewrs +=1
# else:
#     print("Incorrect!")
    
# print(f"Your score: {correct_ansewrs}")

# Quiz Game with lists

print("Python quiz!")

correct_answers = 0

question = ["Question 1. how many loop types are in python?: ",
            "Question 2. what is the method name called to change the string lower?: ",
            "Question 3. True or False. is argument and parameter same?: "]
answer = ["2", "lower", "false"]

for x in range(len(question)):
    question_input = str(input(question[x]))
    if question_input.lower()==answer[x] : 
        print("Correct!")
        correct_answers  +=1
    else: print(f"Incorrect!. Correct answer is {answer[x]}" )    
    
print(f"Your score: {correct_answers }/3")
if(correct_answers==3):
    print("Excellent!")
elif(correct_answers==2):
    print("Good job!")
else:
    print("Keep participating!")