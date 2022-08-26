import os
import argparse
import subprocess
from os.path import exists


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


# Check if Veracrypt is installed
file_exists = exists('/usr/bin/veracrypt')
if file_exists is False:
    print(color.RED + 'You need to install VeraCrypt to execute the program' + color.END)
    quit()

# Check for root privileges
if os.geteuid() != 0:
    print(color.RED + 'You need to be root to execute the program' + color.END)
    quit()

# Intro
print(color.YELLOW + '\n*=*=*= VERADECRYPT =*=*=*' + color.END)
print('This tool aims to unlock Veracrypt volumes using a list of passwords')
print('Arguments: -v for veracrypt volume to crack and -p for password list\n')

# Parse arguments given by user executing the tool
parser = argparse.ArgumentParser(description='VeraCrypt password checker')
parser.add_argument('-v', metavar='volume', type=str, required=True, help='Path to volume')
parser.add_argument('-p', metavar='password_list', type=str, required=True, help='Password list')
args = parser.parse_args()
volume = args.v
plist = args.p

# Checks if arguments exist
vol_exist = exists(volume)
if not vol_exist:
    quit(color.RED + 'Volume does not exist!' + color.END)
pl_exist = exists(plist)
if not pl_exist:
    quit(color.RED + 'Password list does not exist!' + color.END)

# Check if VeraCrypt has a volume mounted on slot 1 (it needs to be free)
print('If VeraDecrypt finds the correct password, it will mount the volume on slot 1')
print('VeraDecrypt will now dismount volumes mounted on slot 1')
print(color.DARKCYAN + 'Save your work before proceding!' + color.END)
tour0 = True
while tour0:
    ans = input(color.DARKCYAN + 'Are you ready? (y/n)\n' + color.END)
    if ans == 'y' or ans == 'Y':
        cmd = 'sudo veracrypt --text --dismount --slot 1'
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        procreturn = str(out, "utf-8").strip() if out else str(err, "utf-8").strip()
        if 'Error:' in procreturn:  # edit for different languages
            print(color.GREEN + 'No volume was mounted, nothing done' + color.END)
        else:
            print(color.GREEN + 'Volume has been dismounted' + color.END)
        tour0 = False
    elif ans == 'n' or ans == 'N':
        print(color.GREEN + 'Ok, nothing done. See you later' + color.END)
        quit()
    else:
        print(color.RED + 'No correct answer provided, try again' + color.END)

# Check number of passwords to check adn show it
f = open(plist, 'r')
n = len(f.readlines())  # number of passwords to check
print(f'- - - - - - - - - -\nChecking {n} passwords...')

# Read file again from the beginning
f.seek(0)
i = 0  # variable to iterate through the password list

skipped = []  # list that will collect skipped password due to not allowed chars

# Checks if password contain characters that will block the tool
wrong_char = ['"', "'", '&', '|']


def check_clean(passwd, wrongs):
    for w in wrongs:
        if w in passwd:
            print(f'Skipping password {passwd} containing unsupported symbols')
            return True
    return False


# Iterates through the passwords and tries to unlock the volume
while i < n:
    password = f.readline()
    password = password.strip()
    print(f'- - - - - - - - - -\nTrying password: {password}')
    if check_clean(password, wrong_char):
        i += 1
        skipped.append(password)
    else:
        cmd = 'sudo veracrypt --text --mount ' + volume + ' /mnt --password ' + password + ' --non-interactive'
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        procreturn = str(out, "utf-8").strip() if out else str(err, "utf-8").strip()
        if 'Error:' in procreturn:  # edit for different languages
            i += 1
            print('Wrong password')
        else:
            print(color.GREEN + f'\n-----PASSWORD FOUND: {password}\n' + color.END)
            os.system('sudo veracrypt --text --dismount --slot 1')
            quit()
print(color.RED + '----------\nPASSWORD NOT FOUND!\nTry another list\n----------' + color.END)
# Prints password skipped to try them manually in GUI version
if (len(skipped)) > 0:
    print(color.CYAN + f'Skipped passwords to try in GUI:' + color.END)
    for pw in skipped:
        print('- ' + pw)
        
