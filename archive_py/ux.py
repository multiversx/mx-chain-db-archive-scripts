def confirm_continuation(yes: bool = False):
    if (yes):
        return

    answer = input("Continue? (y/n)")
    if answer.lower() not in ["y", "yes"]:
        print("Confirmation not given. Will stop.")
        exit(1)
