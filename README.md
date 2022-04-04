# VeraDecrypt.py
Veradecrypt tryes to unlock volumes encrypted with veracrypt trying passwords taken from a desiderd list. It runs under Linux with Python 3.x and needs Veracrypt installed and root privileges. I suggest you to put the script, the volume to decrypt and the password list in the same working directory. You can use the vol_demo and the plist files to test the script in your enviroment.

![VeraDecrypt_Logo](https://github.com/ASeriousMister/VeraDecrypt.py/blob/main/VDC.png?raw=true)

### Example sintax:

``` sudo python3 VeraDecrypt.py -v vol_demo -p plist ```

### Additional notes
For eencrypted devices you can use, i.e. /dev/sdb1 instead of volume name
To know the device name use

``` sudo fdisk -l  ```

when it is connected.

The tool was tested on a system with English language set. If you are using another language and Veracrypt is giving different answers running

``` sudo veracrypt --mount vol_demo /mnt -password password --non-interactive ```

intentionally using a wrong password, edit this line VeraCrypt.py file.

69 ``` if ('Error:' in procreturn): ```

If password is found and the volume gets mounted on slot 1, dismountit with 

``` sudo veracrypt --text --dismount --slot 1 ```

### Disclaimer
Please only use this tool on systems or on volumes you have permission to access! Ethical use only.
Any actions and or activities related to this tool is solely your responsibility.
