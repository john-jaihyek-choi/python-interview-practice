import random


def guessing_game() -> int:
    try:
        available_ranges = [(1, 50), (1, 100), (1, 250), (1, 500), (1, 1000)]
        frm, to = random.choice(available_ranges)
        random_num = random.randint(frm, to)

        while True:
            ans = int(input(f"guess a number from {frm} to {to}: "))

            if ans == random_num:
                print(f"You guessed it correct! ({ans})")
                return ans
            elif ans < random_num:
                print(f"Low!")
            else:
                print(f"High!")
    except ValueError:
        print("Invalid integer format. Please provide integer.")
    except:
        print("unexpected error")


guessing_game()
