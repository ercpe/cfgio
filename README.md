cfgio
=====

cfgio is a python library for reading and writing configuration file formats found on a *nix system. The core goal is to provide an r/w API to files in different formats and still maintaining the overall layout (comments, structure) of the files.


## Why?
Because i often need to read and write configuration files on systems. Typically i `open` the file, read it and use a mix of string functions and regular expression to extract the values i need. When it comes to writing configuration files things get nasty. Have you ever tried to diff a config which has been re-written by a program?

# Examples

**Reading entries from /etc/fstab**

    from cfgio import fstab
    fstab = fstab.FstabRWConfig('/etc/fstab')
    print(fstab.get('/dev/sda2'))
    
    /dev/sda2 on /boot (ext4), opts: noatime,discard (1/2)
