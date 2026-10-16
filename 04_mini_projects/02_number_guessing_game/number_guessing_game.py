# Number guessing game

import random

print("Welcome to the Number Guessing Game!")
print("I'm thinking of a number between 1 and 100.")
print("You have 10 attempts to guess the number.")
print("Good Luck!")

correct_number = random.randint(1, 100)
max_attempts = 10
guess_number = 0
checker = True

while checker:
    try:
        guess = int(input(f"Guess {guess_number + 1}. What is the number?: "))
    except ValueError:
        print("Please enter a valid number.")
        continue

    if not 1 <= guess <= 100:
        print("Please enter a number between 1 and 100.")
        continue

    guess_number += 1

    if guess == correct_number:
        print("You got the number correctly! The number is:", correct_number)
        checker = False
    elif guess > correct_number:
        print("You guessed too high")
    elif guess < correct_number:
        print("You guessed too low")

    if guess_number == max_attempts and guess != correct_number:
        print("You have used all your attempts. The number is:", correct_number)
        checker = False


