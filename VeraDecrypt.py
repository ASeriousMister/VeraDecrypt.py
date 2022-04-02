import os
import argparse
import subprocess
from os.path import exists

#Check if Veracrypt is installed
file_exists = exists('/usr/bin/veracrypt')
if file_exists is False:
    print('You need to install VeraCrypt to execute the program')
    quit()

#Check for root privileges
if os.geteuid() != 0:
    print('You need to be root to execute the program')
    quit()

#intro
print('\n*=*=*= VERADECRYPT =*=*=*\n')
print('This tool aims to unlock Veracrypt volumes using a list of passwords')
print('Arguments: -v for veracrypt volume to crack and -p for password list\n')

#parse arguments given by user executing the tool
parser = argparse.ArgumentParser(description='VeraCrypt Cracker')
parser.add_argument('-v', metavar='volume', type=str,
                    required=True, help='Path to volume')
parser.add_argument('-p', metavar='password', type=str,
                    required=True, help='Password list')
args = parser.parse_args()
volume = args.v
plist = args.p

#Check number of passwords to check adn show it
f = open(plist, 'r')
n = len(f.readlines())  # number of passwords to check
print(f'- - - - - - - - - -\nChecking {n} passwords...')

#Read file again from the beginning
f.seek(0)
i = 0  # variable to iterate through the passowrd list

skipped = []  # list that will collect skipped password due to unallowed chars

#checks if password contain characters that will block the tool
wrong_char = ['"', "'", '&','|']
def check_clean(passwd, wrongs):
    for w in wrongs:
        if w in passwd:
            print(f'Skipping password {passwd} containing unsupported symbols')
            skip = 1
            return True
    return False

#Iterates through the passwords and tries to unlock the volume
while(i < n):
    password = f.readline()
    password = password.strip()
    print(f'- - - - - - - - - -\nTrying password: {password}')
    if check_clean(password, wrong_char):
        i += 1
        skipped.append(password)
    else:
        cmd = 'sudo veracrypt --text --mount ' + volume + \
            ' /mnt --password ' + password + ' --non-interactive'
        process = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        procreturn = str(
            out, "utf-8").strip() if out else str(err, "utf-8").strip()
        if ('Error:' in procreturn):  # edit for different languages
            i += 1
            print('Wrong password')
        else:
            print(f'\n-----PASSWORD FOUND: {password}\n')
            quit()
print('----------\nPASSWORD NOT FOUND!\nTry another list\n----------')
# prints password skipped to try them manually in GUI version
if (len(skipped)) > 0:
    print(f'Skipped passwords to try in GUI: {skipped}')

#To dismount mounted volume sudo veracrypt --text --dismount --slot 1
