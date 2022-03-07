import os
import string
import subprocess

def cls():
    os.system("clear")

def command_subprocess(arg):
    process = subprocess.Popen(arg, shell=True, stdout=subprocess.PIPE)
    output = process.communicate()
    try:
        data: str = output[0].decode()
        lines = data.splitlines()
        return lines
    except IndexError:
        return []


def text_format(arg):
    if arg == "default":
        print("\033[0;37;40m")
    elif arg == "critical":
        print("\033[1;31;40m")
    elif arg == "good":
        print("\033[1;32;40m")
    elif arg == "warning":
        print("\033[0;33;40m")

def gui_welcome_message():
    cls()
    text_format("good")
    print("|===========================================|")
    print("|                                           |")
    print("|           Welcome to symlink.py           |")
    print("|                                           |")
    print("|===========================================|")

def gui_main_menu() -> str:
    text_format("default")
    print("Enter Selection:")
    print(" 1. \033[1;31;40mCreate\033[0;37;40m a shortcut in your home directory. ")
    print(" 2. \033[1;31;40mRemove\033[0;37;40m a shortcut in your home directory.")
    print(" 3. \033[1;31;40mRun shortcut report.")
    text_format("warning"); print("\nPlease enter a number (1-3) or (q/Q) to quit\n"); text_format("default")
    return input(">>> ")

def run_create_sym():
    text_format("warning"); arg = input("Please enter the filename to create a shortcut >>> \033[0;37;40m");
    output = command_subprocess("find $HOME -name " + arg)
    if (len(output) == 0):
        print("No files found, returning to menu...")
    elif (len(output) == 1):
        print("Found one file, " + output)
    else:
        print("Found multiple files:")
        for i in range(0, len(output)):
            print((str)(i) + " : " + output[i])

def run_remove_sym():
    pass

def run_report():
    pass

def main_menu():
    gui_welcome_message()
    while(True):
        output:str = gui_main_menu()
        if output == "1":
            run_create_sym()
        elif output == "2":
            run_remove_sym()
        elif output == "3":
            run_report()
        elif output.lower() == "q":
            text_format("critical"); print("Goodbye!"); text_format("default")
            break
        else:
            text_format("critical"); print("Invalid argument"); text_format("default")

def main():
    main_menu()


main()