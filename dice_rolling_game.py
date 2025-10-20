import random

roll_count = 0

while True:
    choice = input("Roll the dice? (y/n): ").lower()

    if choice == 'y':
        roll_count += 1
        choice_num = int(input("How many dice do you want to roll? "))
        dice_result = []

        for i in range(choice_num):
            roll = random.randint(1, 6)
            dice_result.append(roll)

        print("You Rolled:", dice_result)
        print(f"Total: {sum(dice_result)}")

    elif choice == 'n':
        print("You have rolled (roll_count)so far")
        print("Thanks for playing!")

        break

    else:
        print("Invalid choice! Please enter y or n.")
