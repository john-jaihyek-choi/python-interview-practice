import sys


# sys.argv - useful for automation on cli
def get_cli_arguments() -> str:
    try:
        if len(sys.argv) > 1:
            print(f"cli arguments: {sys.argv}")
        else:
            print(f"no arguments passed in")
    except Exception:
        print("unexpected error")


# exits program gracefully
def run_program() -> str:
    try:
        status = input("run program? (Y:N) ")

        if status in ["Y", "y", "Yes", "yes", "YES"]:
            print("successfully ran program!")
        else:
            print("Program exiting...")
            sys.exit(1)
    except Exception as e:
        print(f"{e}")
        print("Unknown error")


# sets and checks recursion limit
def check_set_recursion_limit() -> None:
    sys.setrecursionlimit(10)
    print(f"recursion limit: {sys.getrecursionlimit()}")
    count = 0

    def recursion():
        nonlocal count
        count += 1
        print(f"recursed {count}")
        recursion()

    try:
        recursion()
    except RecursionError:
        print("recursion depth exceeded...")


get_cli_arguments()
run_program()
check_set_recursion_limit()
