# Table of Contents
- [Table of Contents](#table-of-contents)
- [Prompt](#prompt)
- [Notes](#notes)
    - [Understanding Permissions](#understanding-permissions)
    - [Editing Permissions with Chmod](#editing-permissions-with-chmod)
    - [Finding Files with Certain Permissions](#finding-files-with-certain-permissions)

# Prompt

On UNIX-based systems like OSX, directory and file permissions are generally made up of three groups of three: read, write, and execute permissions for the individual owner, the group owner, and everyone else. You can view the permissions in Terminal with "ls -l" and change the permissions in Terminal with chmod. Create a test file and see what permissions it is given by default, then try changing the permissions on it. Take a look at the permissions of some of the directories and files on your computer. Do they make sense to you? Why do you think they have the permissions they do? 

Optional coding extension: Write a script to find any files in your home directory (your folder in `/Users/`) that are writeable by someone other than you. Do these permissions seem safe to you?

# Notes

## Understanding Permissions
I made the file `a.py` in my `/Users`, and got these results from `ls -l`:

    drwx------@   3 niksure  staff    96 Aug 24 10:27 Applications
    drwx------+  10 niksure  staff   320 Sep 20 15:23 Desktop
    drwx------+   9 niksure  staff   288 Sep 22 10:30 Documents
    drwx------+ 127 niksure  staff  4064 Oct 23 10:03 Downloads
    drwx------@  61 niksure  staff  1952 Sep 25 13:09 Library
    drwx------+   3 niksure  staff    96 Jul 25 09:52 Movies
    drwx------+   4 niksure  staff   128 Aug 24 12:22 Music
    drwx------+   3 niksure  staff    96 Jul 25 09:52 Pictures
    drwxr-xr-x+   4 niksure  staff   128 Jul 25 09:52 Public
    drwxr-xr-x    6 niksure  staff   192 Oct  3 15:47 Shuffleboard
    drwxr-xr-x    2 niksure  staff    64 Oct  3 15:47 SmartDashboard
    -rw-r--r--    1 niksure  staff     0 Oct 23 13:19 a.py
    -rw-r--r--@   1 niksure  staff     1 Aug 24 12:45 a.sh
    drwxr-xr-x    2 niksure  staff    64 Sep 14 14:35 pico_key
    drwxr-xr-x    9 niksure  staff   288 Aug 24 22:36 wpilib

On default, a file that I created in the `/Users` folder, and presumably anywhere else, received these base permissions:

    -rw-r--r-- 

These permissions make sense to me since I have seen them before. The first character, in this case "-", determines whether or not the result is a file or directory (d = directory, - = file), as seen above. The next three characters determine the permissions of the owner of the file/directory, which in the case of the things in my `/Users/` directory, is me. `rw-` means that I have read and write privledges on `a.py`, but do not have execute permissions (because it is a python file, python executes it). The next three characters determine the permissions of the owning group, which is `staff`. The `staff` group has read privledges on this file, but not write or execute privledges. Finally, the last three characters determine the permissions of users who aren't owners of the file or in the owning group. These users have read permissions as well. Finally, in OSX, the `@` symbol at the end of some permission strings means that these files/directories have additional information that can be accessed with `xattr`. 
For example,

    xattr Applications

returns [com.apple.quarantine](https://apple.stackexchange.com/questions/104712/what-causes-os-x-to-mark-a-folder-as-quarantined), which is used to protect users from trojan horse attacks by marking potentially untrustworthy content downloaded from the internet.

## Editing Permissions with Chmod
The permissions of a file can be modified using `chmod` as shown below:

    chmod a.py 664

This command results in the the permission of `a.py` being changed from `-rw-r--r--` to `-rw-rw-r--`. The three numbers represent the new permissions of the owner, owning group, and any users, respectively. In this command, the read privledge is given to any users, which is signified by 4. The read and write privledges are given to the owner and owning group, which means that write permissions have a value of 2. Finally, execute permissions have a value of 1. As seen in the example, the numbers are added depending on what permissions you want to give to each group. For example, 

    chmod a.py 777

gives read, write and execute permissions to every group, which should never be done. Giving everyone all permissions is not a good idea!

## Finding Files with Certain Permissions
To find all files that can be read, written, and executed by the owner, the owning group, and any other users, I can use the `find` command with the number system used above.

    find \Users -perm 777

This command returned 

    ./Library/Application Support/Adobe/OOBE
    ./Library/Application Support/Adobe/Adobe Illustrator 22
    ./Library/Preferences/Adobe Illustrator 22 Settings
    ./Library/Preferences/Adobe/Adobe Illustrator
    ./Library/Logs/CreativeCloud
    ./Library/Logs/CreativeCloud/ACC
    ./Library/Containers/com.apple.geod/Data/Library/Caches/com.apple.geod
    ./Library/Containers/com.apple.geod/Data/Library/Caches/com.apple.geod/MapTiles
    ./Library/Containers/com.apple.geod/Data/Library/Caches/com.apple.geod/PlaceData
    ./Library/Caches/GeoServices/Resources
    ./Library/Caches/GeoServices/RegionalResources

Many of the files in the `Library` directory can be read, written, and executed by any user. For the files mentioned below, I think that this is fine, because many of these scripts are run in the background without my knowledge by applications I have installed.

To search with less of a filter, I used:

    find . -perm -u=w

Which finds all files in the current directory which the user has write permissions on. I can find all files the owning group and read, write, and execute by running:

    find . -perm -g=w+r

Essentially, permissions can be added with the `+` operator. Finally, the permissions we check for can be changed by modifying the `g` for group with `u` for user or `o` for any user. More than one of these conditions can be checked by adding another `-perm` and the permissions we are checking for. For example, 

    find . -perm -u=r+w+x -perm -g=r+w

finds all files and directories in which the user has read, write, and execute permissions, while the owning group has read and write permissions.