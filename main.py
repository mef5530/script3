#!/usr/bin/python3

#Max Friedland
#3/4/22

import os
import subprocess

#clears the terminal
def cls():
    os.system("clear")

#runs the command and returns the output in an array
def command_subprocess(arg):
    process = subprocess.Popen(arg, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    output = process.communicate()
    try:
        data: str = output[0].decode()
        lines = data.splitlines()
        return lines
    except IndexError:
        return []

#checks if the arg is a symlink
def check_symlink(arg):
    output = command_subprocess("readlink " + arg)
    if (len(output) == 1):
        return True
    return False

#helps me format fancy text:)
def text_format(arg):
    if arg == "default":
        print("\033[0;37;40m")
    elif arg == "critical":
        print("\033[1;31;40m")
    elif arg == "good":
        print("\033[1;32;40m")
    elif arg == "warning":
        print("\033[0;33;40m")

#clears screen, displays welcome, shows working dir
def gui_welcome_message():
    cls()
    text_format("good")
    print("|===========================================|")
    print("|                                           |")
    print("|           Welcome to symlink.py           |")
    print("|                                           |")
    print("|===========================================|")
    print("")
    wd = command_subprocess("pwd")
    print("Your current working directory is: " + wd[0])

#displays the main menu and returns the selection
def gui_main_menu() -> str:
    text_format("default")
    print("Enter Selection:")
    print(" 1. \033[1;31;40mCreate\033[0;37;40m a shortcut in your home directory. ")
    print(" 2. \033[1;31;40mRemove\033[0;37;40m a shortcut in your home directory.")
    print(" 3. \033[1;31;40mRun shortcut report.")
    text_format("warning"); print("\nPlease enter a number (1-3) or (quit) to quit\n"); text_format("default")
    return input(">>> ")

#helper to create symlinks (run when user selects 1)
def run_create_sym():
    text_format("warning"); arg = input("Please enter the filename to create a shortcut >>> \033[0;37;40m");
    output:list = command_subprocess("find $HOME -name " + arg)
    for i in range(0, len(output)):
        for e in output:
            if check_symlink(e):
                output.remove(e)
    checkput = command_subprocess("ls -l /$HOME/Desktop/" + arg)
    if "No such file" in checkput[0]:
        if (len(output) == 0):
            text_format("critical"); print("No files found, returning to menu...")
        elif (len(output) == 1):
            print("Found one file, " + output)
            lnoutput = command_subprocess("ln -s " + output[0] + " $HOME/Desktop/" + arg)
            if ("File exists" in lnoutput[0]):
                text_format("critical");
                print("Task failed, file already exists.")
            else:
                print("Task done!")
        else:
            print("Found multiple files:")
            for i in range(0, len(output)):
                print((str)(i) + " : " + output[i])
            text_format("warning"); selection:int = (int) (input("Please enter the index of the file you would like to create the shortcut for. For example, enter 0 for " + output[0] + " >>>\033[0;37;40m "))
            lnoutput = command_subprocess("ln -s " + output[selection] + " $HOME/Desktop/" + arg)
            try:
                if("File exists" in lnoutput[0]):
                    text_format("critical"); print("Task failed, file already exists.")
            except IndexError:
                print("Task done!")
    else:
        text_format("critical"); print("File already exists")

#helper to remove symlinks (selection is 2)
def run_remove_sym():
    fn = input("Enter the name of the link to remove >>> ")
    if check_symlink("/$HOME/Desktop/" + fn):
        resp = input("Are you sure you want to remove " + fn + " (y/N")
        if (resp.lower() == "y"):
            command_subprocess("rm -rf /$HOME/Desktop/" + fn)
            print("Done!")
    else:
        print("That isnt a symlink...")

#helper to run report (selection is 3)
def run_report():
    symlinkcount = 0
    desktopitems = command_subprocess("ls /$HOME/Desktop")
    for e in desktopitems:
        if check_symlink("/$HOME/Desktop/" + e):
            symlinkcount+=1
    print("Number of links is: " + (str)(symlinkcount))
    print("")
    print("Link  :  Target")
    for e in desktopitems:
        if check_symlink("/$HOME/Desktop/" + e):
            print(e + "   :  " + command_subprocess("readlink /$HOME/Desktop/" + e)[0])

#driver for the main menu
def main_menu():
    gui_welcome_message()
    while(True):
        text_format("default")
        output:str = gui_main_menu()
        if output == "1":
            run_create_sym()
        elif output == "2":
            run_remove_sym()
        elif output == "3":
            run_report()
        elif output.lower() == "quit":
            text_format("critical"); print("Goodbye!"); text_format("default")
            break
        else:
            text_format("critical"); print("Invalid argument"); text_format("default")

def main():
    main_menu()


main()