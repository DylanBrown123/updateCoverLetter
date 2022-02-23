#from shutil import copyfile
import shutil
import re
import datetime
# ------------------------------------
#Dylan B Brown's Project - 1/28/2022
#Cmd Prompt UI menu for updating coverletter in local client.
#Will make second E2E version
#----    ----    ----    ----    ----
print("_.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-.\n"
      "Disclaimer: In the current version, I only work with text files.\n"
      "I work best on windows OS, and have not been tested with Apple M1 chips."
      "\n_.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-.")

# Function description: Menu design, text only
def print_menu():
    print("\n")
    print(30 * "-", "MENU", 30 * "-")
    print("1. Read CV File")
    print("2. Update CV File")
    print("3. Update Company Name")
    print("4. Menu Option 4")
    print("5. Exit")
    print(67 * "-")

# Function description: Open & Read Text File (CV), if user chose 2, updates file contents to current date
#            Called in:
def replaceLoop(oldVal,newVal,file_name):
    fin = open(file_name, "r")
    # Loop through string & replace oldDate with current_date
    replacement = ""
    for line in fin:
        line = line.strip()  # Removes all whitespace from begining and end of line string
        changes = line.replace(oldVal, newVal)
        replacement = replacement + changes + "\n"
    fin.close()
    # open the file in write mode, update file with replacement string
    fout = open(file_name, "w")
    fout.write(replacement)
    fout.close()

# Function description: Open & Read Text File (CV), if user chose 2, updates file contents to current date.
#            Called in: Menu while loop, option 1 & 2
def readFile(userInput):
    if ".txt" not in userInput:     #If user input file name does not contain TXT extension, append it.
        userInput += ".txt"

    fin = open(userInput, "r")      # open&read input txt file, fin
                                    # If chose to update, update to current date. !!!Overwrites original!
    if choice == "2":
        text = fin.read()
        # match a regex pattern for formatted dates
        datePattern = "\d{2}[/-]\d{2}[/-]\d{4}"
        global oldDate
        oldDate = re.findall(datePattern, text)  # Finds dates in file text (with #/#/# format)
        oldDate = oldDate[0]
        current_date = datetime.date.today()
        curr_date_Str = current_date.strftime("%m-%d-%Y")  # Converting datetime object to string

        # Close and open - to try and not leave the "cursor" to already start at end of loop for "fin".
        fin.close()
        replaceLoop(oldDate,curr_date_Str,userInput)

    elif choice == "3":
        #text = fin.read()
        oldCompany = input("\nWhat company name are we replacing?: ")
        newCompany = input("\nWhat is the name of the new company you're applying to?: ")

        fin.close()
        replaceLoop(oldCompany, newCompany, userInput)

    fout = open(userInput, "r")
    print(30 * "-", "File", 30 * "-")
    print(fout.read())
    print(67 * "-")
    fout.close()
    #print("\n")
    return userInput

#Format Checks strings if they end with fwd- or back-slash. If not, appends backslash.
def lastCharSlash(string):
    last_char = string[-1]
    if last_char != "/" and last_char != "\\":
        print("\nMSG: File path does not end with forward or backward slash, appending backslash.")
        string = string + "\\"
    else:
        print("\nMSG: Text DOES end with forward or backward slash, no alteration required.")
    return string

fin = None            ##Prevents 'undefined' error, in the case of skipping option 1 & going option 2. ??Might move up.

## While loop description: Loop will keep going until loop = False; Contains menu actions
##                  Calls: print_menu(), readFile(), getCV(), shutil.copyfile
loop = True
while loop:
    print_menu()      ## Displays menu text
    choice = input("Enter your choice [1-5]: ")

    if choice == "5" or len(choice) == 0:
        print("Exiting Program.")
        loop = False  # This will make the while loop to end as not value of loop is set to False

    elif choice == "1":
        print("Choice 1 - open CV file - has been selected.")

        # Method descr: - Open/read CV - Note may circle back and add a passable param to specify which CV to open
        # Calls function: - readFile
        ## ??? Note, might be redundant, check back.
        def getCV():
            print("\nType 'h' for help.\n")
            fileNam = input("Which CV file would you like to view?: ")
            if len(fileNam) == 0:   #If user enters no input, quit
                quit()
            elif fileNam == "h":    #'h' displays help text
                print("\nIf you're not currently in same directory as your file, you may need to specify the filepath.")
            elif fileNam == "":     #???Possibly redundant
                quit(getCV())
            else:                   #Open & reads user input text file, if file exists in directory/directory specified.
                fin = readFile(fileNam)
                return fin
        fin = getCV()               # input file name (Global var)

    elif choice == "2":
        if fin:                           # Checks for last CV file read (Menu opt 1) during current process
            print("\nChoice 2 selected, updating " + fin)
        else:                             # If user skipped menu choice #1, prompt user for file name, fin
            fileNam = input("Which file would you like to update?: ")
            fin = readFile(fileNam)

        saveMethod = input("\nType 'c' to save as a separate updated copy, or 'o' to overwrite " + fin + ": \n")
        if len(saveMethod) == 0:
            quit()
        # <<<Save as copy of 'fin' (orig CV)>>>
        elif saveMethod == "c":
            origFpath = input("\nHelp me find the file path of the file to be copied,\n"
                              "Example: C:/Users/Smith/Desktop/Test_1 \n"
                              "Please indicate the original path where the file (to be copied) is currently stored\n"
                              "Copy from path: ")
            if len(origFpath) == 0:
                quit()
            origFpath = lastCharSlash(origFpath)
            origFpath = origFpath + fin     # origFpath now format-checked (with file name, path, backslash, & type)

            # <<<Get new file name.txt>>>
            newFileNam = input("\nName of your new CV template? (!!DO NOT ADD '.txt' file extension!!)\n"
                               "New file name: ")
            newFileNam = newFileNam + ".txt"

            # <<<Get Target File Path for Copy>>>
            targetFpath = input("\nWhere would you like to save the copied CV txt file?\n"
                                "(Replace fwd slash with backslashes) Example: C:/Users/Smith/Desktop/Test_2/ \n"
                                "Target save path: ")
            if len(targetFpath) == 0:
                quit()
            targetFpath = lastCharSlash(targetFpath)
            targetFpath = targetFpath + newFileNam
            print("\nSaving from: " + origFpath +
                  "\nto: " + targetFpath + "...")

            shutil.copyfile(origFpath, targetFpath)     #Copies original file to target filepath as separate new CV template
            #nfin = open(newFileNam, "x")    ##??? Check back here and see if can just name nfin as existing fin var

        elif saveMethod == "o":
            print("This feature will be made available in future versions. Please save as separate copy for now.")

        #del choice      #Probably don't need to delete this variable b/c it just gets overwritten in while loop

    elif choice == "3":
        if fin:                           # Checks for last CV file read (Menu opt 1) during current process
            print("\nChoice 3 selected, updating company name in " + fin)
        else:                             # If user skipped menu choice #1, prompt user for file name, fin
            fileNam = input("\n Choice 3 selected\nWhich file would you like to update?: ")
            fin = readFile(fileNam)

    elif choice == "4":
        print("Menu 4 has been selected")
        ## You can add your code or functions here
    else:
        # Any integer inputs other than values 1-5 we print an error message
        print("Wrong option selection. Enter any key to try again..")

quit()

#if fin:  fin.close()  <-- Considering always closing file at end of program?