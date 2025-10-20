import random

random_num = random.randint(1, 100)
while True:
    try:
        guessed_number = int(input("Guess the number between 1 and 100: "))
        
        if guessed_number > random_num:
            print("Too high")
        elif guessed_number < random_num:
            print("Too low")
        else:
            print("Bravo, you did it right!")
            break
    except ValueError:
        print("Please enter a valid number")